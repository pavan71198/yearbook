from .models import Profile


def generate_username(backend, response, details, *args, **kwargs):
    if backend.name == 'azuread-tenant-oauth2':
        details['username'] = response['unique_name'].split('@')[0]


def create_new_profile(backend, user, response, details, *args, **kwargs):
    if backend.name == 'azuread-tenant-oauth2':
        if Profile.objects.filter(user=user).count()==0:
            rollno = details['last_name']
            year = 2000+int(rollno[:2])
            program = rollno[2:4]
            department = rollno[4:6]
            graduating = True
            if year != 2015 and (program == "01" or program == "02"):
                graduating = False
            Profile.objects.create(user=user, full_name=response['name'], department=department, program=program, rollno=int(rollno), graduating=graduating)
