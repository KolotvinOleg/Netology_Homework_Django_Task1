import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_one_course(client, course_factory):
    course = course_factory()
    response = client.get('/api/v1/courses/1/')
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 3
    assert data['id'] == course.id
    assert data['name'] == course.name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    count = Course.objects.count()
    courses = course_factory(_quantity=10)
    assert Course.objects.count() == count + 10
    response = client.get('/api/v1/courses/')
    assert response.status_code == 200
    data = response.json()
    for i, course in enumerate(data):
        assert course['id'] == courses[i].id
        assert course['name'] == courses[i].name


@pytest.mark.django_db
def test_filter_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)
    for course in courses:
        url = '/api/v1/courses/' + f'?id={course.id}'
        response = client.get(url)
        data = response.json()
        assert response.status_code == 200
        assert data[0]['id'] == course.id
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_filter_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    for course in courses:
        url = '/api/v1/courses/' + f'?name={course.name}'
        response = client.get(url)
        data = response.json()
        assert response.status_code == 200
        assert data[0]['id'] == course.id
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'History'}, format='json')
    data = response.json()
    assert response.status_code == 201
    assert data['name'] == 'History'
    assert data['students'] == []


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    for course in courses:
        response = client.patch(f'/api/v1/courses/{course.id}/', data={'name': 'update_test'})
        data = response.json()
        assert response.status_code == 200
        assert data['name'] == 'update_test'

        response = client.put(f'/api/v1/courses/{course.id}/', data={'name': 'update_test'})
        data = response.json()
        assert response.status_code == 200
        assert data['name'] == 'update_test'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    count = Course.objects.count()
    for course in courses:
        response = client.delete(f'/api/v1/courses/{course.id}/')
        assert response.status_code == 204
    assert Course.objects.count() == count - 10
