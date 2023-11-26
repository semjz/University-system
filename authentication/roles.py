from rolepermissions.roles import AbstractUserRole


class ITManagerRole(AbstractUserRole):
    role_name = "IT Manager"
    available_permissions = {
        'create_student': True,
    }


class AssistantRole(AbstractUserRole):
    role_name = "Assistant"
    available_permissions = {
        'create_student': False,
    }


class ProfessorRole(AbstractUserRole):
    role_name = "Professor"
    available_permissions = {
        'create_student': False,
    }


class StudentRole(AbstractUserRole):
    role_name = "Student"
    available_permissions = {
        'create_student': False,
    }
