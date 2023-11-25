COURSE_TYPES = [
    ("general", "General"),
    ("specialized", "Specialized"),
    ("core", "Core"),
    ("optional", "Optional")
]

MILITARY_STATUS_CHOICES = [
    ("permanent_exemption", "Permanent Exemption"),
    ("education_exemption", "Education Exemption"),
    ("end_of_service", "End of Service"),
    ("included", "Included"),
]
ENTRANCE_TERM_CHOICES = [
    ("Mehr", "Mehr"),
    ("Bahman", "Bahman"),
]
STAGE_CHOICES = [
    ("associate", "Associate"),
    ("bachelor", "Bachelor"),
    ("master", "Master"),
    ("phd", "PHD"),
]
COURSE_CONDITION_CHOICES = [
    ("failed", "Failed"),
    ("passed", "Passed"),
]

PROFESSOR_RANK_CHOICES = [
    ('instructor', 'Instructor'),  # morabi
    ('assistant_professor', 'Assistant Professor'),  # ostadyar
    ('associate_professor', 'Associate Professor'),  # daneshyar
    ('full_professor', 'Full Professor'),  # ostad tamam
]

REQUEST_RESULT_CHOICES = [
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('pending', 'Pending'),
]

GENDERS_CHOICES = [("male", "male"), ("female", "female")]

ROLES_CHOICES = [("Student", "Student"), ("Professor", "Professor"), ("Assistant", "Assistant")
    , ("IT Manager", "It Manager"), ("Super Admin", "Super Admin")]
