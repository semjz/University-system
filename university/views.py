from django.http import HttpResponse
from .tasks import test_func
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsItManager
from .models import Student
from .serializers import CreatStudentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def test(request):
    test_func.delay()
    return HttpResponse('Done')

class CreatStudent(CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated, IsItManager)
    serializer_class = CreatStudentSerializer
#alikh
class CreateFacultyView(APIView):
    def post(self, request):
        # دریافت داده‌های ارسال شده
        data = request.data

        # ایجاد دانشکده با استفاده از داده‌های دریافت شده
        # به طور مثال:

        faculty = Faculty.objects.create(

            # فیلدهای دیگر به عهده خودتان است
        )

        # بازگشت پاسخ موفقیت‌آمیز
        return Response(status=status.HTTP_201_CREATED)


class ListFacultiesView(APIView):
    def get(self, request):
        # دریافت لیست دانشکده‌ها
        faculties = Faculty.objects.all()

        # تبدیل لیست دانشکده‌ها به فرمتی که مدنظرتان است
        # به طور مثال، تبدیل به JSON
        faculty_list = [{'name': faculty.name} for faculty in faculties]

        # بازگشت لیست دانشکده‌ها
        return Response(faculty_list)

class RetrieveFacultyView(APIView):
    def get(self, request, pk):
        try:
            # یافتن دانشکده با استفاده از شناسه (pk) درخواست شده
            faculty = Faculty.objects.get(pk=pk)

            # تبدیل اطلاعات دانشکده به فرمت مورد نظرتان
            # به طور مثال، تبدیل به JSON
            faculty_data = {'name': faculty.name}

            # بازگشت اطلاعات دانشکده
            return Response(faculty_data)
        except Faculty.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateFacultyView(APIView):
    def put(self, request, pk):
        try:
            # یافتن دانشکده با استفاده از شناسه (pk) درخواست شده
            faculty = Faculty.objects.get(pk=pk)

            # دریافت داده‌های ارسال شده
            data = request.data

            # به روزرسانی فیلدهای دانشکده با استفاده از داده‌های دریافت شده
            # به طور مثال:
            faculty.name = data['name']
            faculty.department = data['department']
            # فیلدهای دیگر به عهده خودتان است

            # ذخیره تغییرات
            faculty.save()

            # بازگشت پاسخ موفقیت‌آمیز
            return Response({'message': 'اطلاعات دانشکده با موفقیت به روزرسانی شد'})
        except Faculty.DoesNotExist:
            return Response({'message': 'دانشکده مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

class DeleteFacultyView(APIView):
    def delete(self, request, pk):
        try:
            # یافتن دانشکده با استفاده از شناسه (pk) درخواست شده
            faculty = Faculty.objects.get(pk=pk)

            # حذف دانشکده
            faculty.delete()

            # بازگشت پاسخ موفقیت‌آمیز
            return Response({'message': 'دانشکده با موفقیت حذف شد'})
        except Faculty.DoesNotExist:
            return Response({'message': 'دانشکده مورد نظر یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

class ListStudentsView(APIView):
    def get(self, request):
        # دریافت لیست دانشجوها
        students = Student.objects.all()

        # اعمال فیلترهای مورد نظرتان
        # به طور مثال، فیلتر بر اساس دانشکده
        school = request.query_params.get('school')
        if school:
            students = students.filter(school=school)

        # تبدیل لیست دانشجوها به فرمت مورد نظرتان
        # به طور مثال، تبدیل به JSON
        student_list = [{'student_id': student.user} for student in students]

        # بازگشت لیست دانشجوها
        return Response(student_list)

class ListProfessorsView(APIView):
    def get(self, request):
        # دریافت لیست استادان
        professors = Professor.objects.all()

        # اعمال فیلترهای مورد نظرتان
        # به طور مثال، فیلتر بر اساس دانشکده
        school = request.query_params.get('school')
        if school:
            professors = professors.filter(school=school)

        # تبدیل لیست استادان به فرمت مورد نظرتان
        # به طور مثال، تبدیل به JSON
        professor_list = [{'user': professor.user} for professor in professors]

        # بازگشت لیست استادان
        return Response(professor_list)

