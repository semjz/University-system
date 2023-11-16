from rolepermissions.roles import AbstractUserRole


class ITManager(AbstractUserRole):
    role_name = "IT Manager"
    available_permissions = {
        'create_student': True,
    }


class Assistant(AbstractUserRole):
    role_name = "Assistant"
    available_permissions = {
        'create_student': False,
    }


class Professor(AbstractUserRole):
    role_name = "Professor"
    available_permissions = {
        'create_student': False,
    }


class Student(AbstractUserRole):
    role_name = "Student"
    available_permissions = {
        'create_student': False,
    }
