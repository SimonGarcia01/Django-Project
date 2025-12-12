from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from login.models import Faculty
from activities.models import Activity, Enrollment, ActivityReview, Participation
from activities.models import ActivityType, CategoryType

User = get_user_model()


class GeneralReportsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        admin_group, _ = Group.objects.get_or_create(name='admin')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.user.groups.add(admin_group)
        self.user.save()
        self.client.login(username='testuser', password='testpass123')
        
        self.faculty = Faculty.objects.create(name='Ingeniería')
        self.activity = Activity.objects.create(
            name='Test Activity',
            type=ActivityType.DEPORTIVA,
            category=CategoryType.GRUPAL,
            is_published=True,
            requires_registration=True,
            max_capacity=10
        )
        Enrollment.objects.create(user=self.user, activity=self.activity)

    def test_general_reports_view_loads(self):
        url = reverse('reportsAndStats:general_reports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Total:')
        self.assertContains(response, 'Actividades')

    def test_general_reports_view_context(self):
        url = reverse('reportsAndStats:general_reports')
        response = self.client.get(url)
        context = response.context
        self.assertIn('total_users', context)
        self.assertIn('total_activities', context)
        self.assertIn('total_enrollments', context)
        self.assertIn('total_reviews', context)
        self.assertIn('published_activities', context)
        self.assertIn('requires_registration', context)
        self.assertIn('activities_with_participants', context)
        self.assertIn('avg_enrollments_per_activity', context)
        self.assertIn('avg_rating', context)
        self.assertIn('unread_reviews', context)
        self.assertIn('users_sample', context)
        self.assertIn('faculties_sample', context)
        self.assertIn('activities_sample', context)
        self.assertIn('top_activities', context)
        self.assertIn('faculty_distribution', context)
        self.assertIn('top_users', context)

    def test_general_reports_view_counts(self):
        url = reverse('reportsAndStats:general_reports')
        response = self.client.get(url)
        context = response.context
        self.assertGreaterEqual(context['total_users'], 1)
        self.assertGreaterEqual(context['total_activities'], 1)
        self.assertGreaterEqual(context['total_enrollments'], 1)
        self.assertGreaterEqual(context['total_faculties'], 1)

    def test_general_reports_view_samples(self):
        url = reverse('reportsAndStats:general_reports')
        response = self.client.get(url)
        context = response.context
        self.assertIsInstance(context['users_sample'], list)
        self.assertIsInstance(context['faculties_sample'], list)
        self.assertIsInstance(context['activities_sample'], list)
        self.assertTrue(hasattr(context['top_activities'], '__iter__'))
        self.assertIsInstance(context['faculty_distribution'], dict)
        self.assertTrue(hasattr(context['top_users'], '__iter__'))


class FilteredReportsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        admin_group, _ = Group.objects.get_or_create(name='admin')
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            gender='M'
        )
        self.user.groups.add(admin_group)
        self.user.save()
        self.client.login(username='testuser', password='testpass123')
        
        self.faculty = Faculty.objects.create(name='Ingeniería')
        self.user.faculty = self.faculty
        self.user.save()
        
        self.activity = Activity.objects.create(
            name='Test Activity',
            type=ActivityType.DEPORTIVA,
            category=CategoryType.GRUPAL,
            is_published=True,
            requires_registration=True,
            max_capacity=10
        )
        self.enrollment = Enrollment.objects.create(user=self.user, activity=self.activity)
        self.review = ActivityReview.objects.create(
            activity=self.activity,
            user=self.user,
            rating=5,
            comment='Great activity'
        )

    def test_filtered_reports_view_actividad_filter(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('data', context)
        self.assertIn('filters', context)
        self.assertIn('selected_filter', context)
        self.assertEqual(context['selected_filter'], 'actividad')
        self.assertIn('Test Activity', context['data'])

    def test_filtered_reports_view_facultad_filter(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'facultad'})
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('data', context)
        self.assertEqual(context['selected_filter'], 'facultad')
        self.assertIn('Ingeniería', context['data'])

    def test_filtered_reports_view_genero_filter(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'genero'})
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIn('data', context)
        self.assertEqual(context['selected_filter'], 'genero')
        self.assertIn('Masculino', context['data'])

    def test_filtered_reports_view_default_filter(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['selected_filter'], 'actividad')

    def test_filtered_reports_view_actividad_data_structure(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        context = response.context
        activity_data = context['data'].get('Test Activity')
        self.assertIsNotNone(activity_data)
        self.assertIn('participacion', activity_data)
        self.assertIn('actividades', activity_data)
        self.assertIn('participaciones_reales', activity_data)
        self.assertIn('tipo', activity_data)
        self.assertIn('categoria', activity_data)
        self.assertIn('ubicacion', activity_data)
        self.assertIn('capacidad_actual', activity_data)
        self.assertIn('capacidad_maxima', activity_data)
        self.assertIn('tasa_participacion', activity_data)
        self.assertIn('rating_promedio', activity_data)
        self.assertIn('total_resenas', activity_data)
        self.assertIn('distribucion_genero', activity_data)
        self.assertIn('distribucion_facultad', activity_data)
        self.assertIn('requiere_inscripcion', activity_data)
        self.assertIn('publicada', activity_data)

    def test_filtered_reports_view_facultad_data_structure(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'facultad'})
        context = response.context
        faculty_data = context['data'].get('Ingeniería')
        self.assertIsNotNone(faculty_data)
        self.assertIn('participacion', faculty_data)
        self.assertIn('actividades', faculty_data)
        self.assertIn('inscripciones', faculty_data)
        self.assertIn('participaciones_reales', faculty_data)
        self.assertIn('actividades_unicas', faculty_data)
        self.assertIn('distribucion_genero', faculty_data)
        self.assertIn('distribucion_tipo_actividad', faculty_data)
        self.assertIn('top_actividades', faculty_data)
        self.assertIn('rating_promedio_dado', faculty_data)
        self.assertIn('total_resenas', faculty_data)
        self.assertIn('tasa_participacion', faculty_data)

    def test_filtered_reports_view_genero_data_structure(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'genero'})
        context = response.context
        gender_data = context['data'].get('Masculino')
        self.assertIsNotNone(gender_data)
        self.assertIn('participacion', gender_data)
        self.assertIn('actividades', gender_data)
        self.assertIn('inscripciones', gender_data)
        self.assertIn('participaciones_reales', gender_data)
        self.assertIn('actividades_unicas', gender_data)
        self.assertIn('distribucion_facultad', gender_data)
        self.assertIn('distribucion_tipo_actividad', gender_data)
        self.assertIn('top_actividades', gender_data)
        self.assertIn('rating_promedio_dado', gender_data)
        self.assertIn('total_resenas', gender_data)
        self.assertIn('promedio_inscripciones_por_usuario', gender_data)
        self.assertIn('tasa_participacion', gender_data)

    def test_filtered_reports_view_actividad_participation_count(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        context = response.context
        activity_data = context['data'].get('Test Activity')
        self.assertGreaterEqual(activity_data['participacion'], 1)
        self.assertGreaterEqual(activity_data['actividades'], 1)

    def test_filtered_reports_view_actividad_rating(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        context = response.context
        activity_data = context['data'].get('Test Activity')
        self.assertGreaterEqual(activity_data['total_resenas'], 1)
        self.assertNotEqual(activity_data['rating_promedio'], 'N/A')

    def test_filtered_reports_view_empty_data(self):
        Activity.objects.all().delete()
        Enrollment.objects.all().delete()
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertIsInstance(context['data'], dict)

    def test_filtered_reports_view_with_participation(self):
        Participation.objects.create(
            activity=self.activity,
            user=self.user,
            attendance_date='2025-01-15'
        )
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        context = response.context
        activity_data = context['data'].get('Test Activity')
        self.assertGreaterEqual(activity_data['participaciones_reales'], 1)

    def test_filtered_reports_view_faculty_enrollments(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'facultad'})
        context = response.context
        faculty_data = context['data'].get('Ingeniería')
        self.assertGreaterEqual(faculty_data['participacion'], 1)
        self.assertGreaterEqual(faculty_data['actividades'], 1)

    def test_filtered_reports_view_gender_enrollments(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'genero'})
        context = response.context
        gender_data = context['data'].get('Masculino')
        self.assertGreaterEqual(gender_data['participacion'], 1)
        self.assertGreaterEqual(gender_data['actividades'], 1)

    def test_filtered_reports_view_contains_overview_table(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'overview-table')

    def test_filtered_reports_view_contains_stats_cards(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'stats-container')

    def test_filtered_reports_view_template_renders(self):
        url = reverse('reportsAndStats:filtered_reports')
        response = self.client.get(url, {'filter': 'actividad'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportsAndStats/filteredReports.html')

    def test_general_reports_view_template_renders(self):
        url = reverse('reportsAndStats:general_reports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportsAndStats/generalReportsAndStatsView.html')
