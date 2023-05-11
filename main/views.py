from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import MentorSignUpForm, MentorTagForm, MenteeSignUpForm, MenteeTagForm, AppointmentUpdateForm, MentorEditProfileForm, MenteeEditProfileForm, MentorBioUpdateForm, MENTEE_QUESTIONS_DICT
from .models import MentorTags, CustomUser, MentorProfile, MenteeProfile, MenteeTags, Appointment, MentorMenteeScore
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import operator, datetime,pytz
from random import shuffle
from .tasks import send_email_task
from datetime import timedelta

def handler404(request,exception):
    return render(request, 'main/404.html', status=404)

def handler500(request):
    return render(request, 'main/500.html', status=500)

def home_view(request):
    return render(request, 'main/home.html')

def signup(request):
    return render(request, 'main/signup.html')

def resources(request):
    return redirect('https://resources-page-b67816.webflow.io/')
    return render(request, 'main/resources.html')

def about(request):
    return render(request, 'main/about.html')

def mentor_details(request):
    return render(request, 'main/mentor_details.html')

def approval_message(request):
    return render(request, 'main/approval_message.html')

@login_required
def mentee_dashboard(request):
    x=[]
    if request.user.is_mentee:
        mentee = MenteeProfile.objects.get(user = request.user)
        x = Appointment.objects.filter(mentee = mentee)
    else:
        x = None
    return render(request, 'main/mentee_dashboard.html',{'x': x})

@login_required
def mentor_dashboard(request):
    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST)
        if form.is_valid():
            appointment_id = form.cleaned_data.get('appointment_id')
            appointment = Appointment.objects.get(id = appointment_id)
            appointment.datetime = datetime.datetime.utcfromtimestamp(form.cleaned_data.get('timestamp'))
            appointment.accepted_by_mentor = True
            appointment.save()
            mentor_reminder_time = appointment.datetime - timedelta(hours=8, minutes=30)
            mentee_reminder_time = appointment.datetime - timedelta(hours=15, minutes=30)

            current_site = get_current_site(request)
            subject = 'Woohoo! 🎉 A New Meeting has been Scheduled'
            message = render_to_string('main/new_meeting_scheduled_email.html', {
                'mentor': appointment.mentor,
                'mentee': appointment.mentee,
                'date': appointment.datetime.strftime("%A, %d %b %Y"),
                'time': appointment.datetime.strftime("%H:%M %p"),
            })
            to = [appointment.mentee.mentee_email, appointment.mentor.mentor_email]
            message.content_subtype = 'html'
            send_email_task.delay(subject, message, to)

            current_site = get_current_site(request)
            subject = '⏰ Reminder for your call today!'
            message = render_to_string('main/mentee_reminder_email.html', {
                'mentor': appointment.mentor,
                'mentee': appointment.mentee,
            })
            to = [appointment.mentee.mentee_email]
            message.content_subtype = 'html'
            send_email_task.apply_async((subject, message, to), eta=mentee_reminder_time)

            current_site = get_current_site(request)
            message = render_to_string('main/mentor_reminder_email.html', {
                'mentor': appointment.mentor,
                'mentee': appointment.mentee,
            })
            to = [appointment.mentor.mentor_email]
            message.content_subtype = 'html'
            send_email_task.apply_async((subject, message, to), eta=mentor_reminder_time)
            return redirect('mentor_scheduled')
    else:
        form = AppointmentUpdateForm()

    appointments = None
    if request.user.is_mentor:
        mentor = MentorProfile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mentor = mentor, accepted_by_mentor = False, rejected_by_mentor = False)
    return render(request, 'main/mentor_dashboard.html', {'appointments': appointments, 'form': form })

def browse(request):
    mentors_user = CustomUser.objects.filter(is_mentor=True, admin_approved=True)
    mentors=[]
    for mentor in mentors_user:
        mentors.append(MentorProfile.objects.get(user=mentor))

    mentor_id_list = []
    recommendation = []
    if request.user.is_authenticated and request.user.is_mentee:
        mentee = MenteeProfile.objects.get(user = request.user)
        booked_mentors = Appointment.objects.filter(mentee = mentee).values('mentor')
        for b in booked_mentors.values():
            mentor_id_list.append(b['mentor_id'])

        score_data_list = MentorMenteeScore.objects.filter(mentee=mentee)
        print(score_data_list)

        if(len(score_data_list)<=3):
            recommendation = score_data_list
        else:
            sorted_score_data_list = sorted(score_data_list,key=operator.attrgetter("score"),reverse=True)
            highest_score_list = []
            highest_score = sorted_score_data_list[0].score
            for score_data in sorted_score_data_list:
                if score_data.score == highest_score:
                    highest_score_list.append(score_data)

            if(len(highest_score_list)>=3):
                shuffle(highest_score_list)
                recommendation = highest_score_list[:3]
                print(recommendation)
            else:
                recommendation=highest_score_list
                remaining_spots = 3 - len(highest_score_list)
                remaining_sorted_score_list = sorted_score_data_list[len(highest_score_list):]
                for x in range(0, remaining_spots):
                    recommendation.append(remaining_sorted_score_list[x])

        # for score_data in score_data_list:
        #     top_score_list =
    # else:
    #     booked_mentors = None
    return render(request, 'main/browse.html', {'mentors': mentors, 'mentor_id_list': mentor_id_list, 'recommendation': recommendation})

@login_required
def admin_dashboard(request):
    new_mentors = CustomUser.objects.filter(is_mentor=True, email_confirmed=True, admin_approved=False)
    return render(request, 'main/admin_dashboard.html', {'new_mentors': new_mentors})

def login(request):
    if request.method == 'POST':
        # Get form values
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_mentor:
                if user.mentorprofile.bio_updated:
                    return redirect('mentor_dashboard')
                else:
                    return redirect('mentor_bio_update')
            elif user.is_mentee:
                return redirect('browse')
            elif user.is_admin:
                return redirect('admin_dashboard')
            print("matched none")
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'main/login.html')

def mentee_signup(request):
    if request.method == 'POST':
        form = MenteeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_mentee = True
            user.is_active = False
            user.save()
            mentee = MenteeProfile.objects.create(user = user)
            # user.refresh_from_db()  # load the profile instance created by the signal
            mentee.mentee_first_name = form.cleaned_data.get('first_name')
            mentee.mentee_last_name = form.cleaned_data.get('last_name')
            mentee.mentee_email = form.cleaned_data.get('email')
            mentee.url = form.cleaned_data.get('url')
            mentee.place_of_work = form.cleaned_data.get('place_of_work')
            mentee.field_of_design = form.cleaned_data.get('field_of_design')
            mentee.bio = form.cleaned_data.get('bio')
            mentee.question1 = MENTEE_QUESTIONS_DICT[form.cleaned_data.get('question1')]
            mentee.question1_answer = form.cleaned_data.get('question1_answer')
            mentee.question2 = MENTEE_QUESTIONS_DICT[form.cleaned_data.get('question2')]
            mentee.question2_answer = form.cleaned_data.get('question2_answer')
            mentee.question3 = MENTEE_QUESTIONS_DICT[form.cleaned_data.get('question3')]
            mentee.question3_answer = form.cleaned_data.get('question3_answer')
            tags = form.cleaned_data.get('tag')
            print(tags)
            for t in tags:
                mentee.tag.add(MenteeTags.objects.get(tag=t.tag))
            mentee.save()

            #Creating Score Table Entries for new Mentee
            for mentor in MentorProfile.objects.filter(field_of_design=mentee.field_of_design):
                score = 0
                for t_mentee in mentee.tag.all():
                    for t_mentor in mentor.tag.all():
                        if(t_mentee.match_id == t_mentor.match_id):
                            score+=1
                MentorMenteeScore.objects.create(score=score,mentor=mentor,mentee=mentee)

            current_site = get_current_site(request)
            subject = 'Mail Verification ✅'
            message = render_to_string('main/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to = [user.email]
            message.content_subtype = 'html'
            send_email_task.delay(subject, message, to)
            return render(request, 'main/account_activation_sent_mentee.html', {'email': mentee.mentee_email})
    else:
        form = MenteeSignUpForm()
    return render(request, 'main/mentee_signup.html', {'form': form})

def mentor_signup(request):
    if request.method == 'POST':
        form = MentorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_mentor = True
            user.is_active = False
            user.save()
            mentor = MentorProfile.objects.create(user = user)
            # user.refresh_from_db()  # load the profile instance created by the signal
            mentor.mentor_first_name = form.cleaned_data.get('first_name')
            mentor.mentor_last_name = form.cleaned_data.get('last_name')
            mentor.mentor_email = form.cleaned_data.get('email')
            mentor.url = form.cleaned_data.get('url')
            mentor.social_url = form.cleaned_data.get('social_url')
            mentor.place_of_work = form.cleaned_data.get('place_of_work')
            mentor.field_of_design = form.cleaned_data.get('field_of_design')
            # mentor.bio = form.cleaned_data.get('bio')
            tags = form.cleaned_data.get('tag')
            bio = "Hey there! I'm "+ mentor.mentor_first_name +" "+ mentor.mentor_last_name+" currently at "+mentor.place_of_work+" and I'd love to get on a call with you! You can talk to me about "
            print(tags)
            tags_length = len(tags)
            curr_tag = 0
            for t in tags:
                curr_tag = curr_tag + 1
                mentor_tag_object = MentorTags.objects.get(tag=t.tag)
                mentor.tag.add(mentor_tag_object)
                if tags_length == 1:
                    bio += mentor_tag_object.tag_auto_bio +"!"
                elif tags_length == curr_tag:
                    bio += "and "+mentor_tag_object.tag_auto_bio +"!"
                else:
                    bio += mentor_tag_object.tag_auto_bio +", "
            mentor.bio = bio
            mentor.save()
            # user.is_mentor = True

            current_site = get_current_site(request)
            subject = 'Mail Verification ✅'
            message = render_to_string('main/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to = [user.email]
            message.content_subtype = 'html'
            send_email_task.delay(subject, message, to)
            return render(request, 'main/account_activation_sent_mentor.html', {'email': mentor.mentor_email})
            # email = form.cleaned_data.get('email')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(email=email, password=raw_password)
            # login(request, user)
            # return redirect('home')
    else:
        form = MentorSignUpForm()
    return render(request, 'main/mentor_signup.html', {'form': form})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None:
        user.email_confirmed = True
        if user.is_mentor:
            user.is_active = False
            user.save()
            return render(request, 'main/approval_message.html')
        else:
            user.is_active = True
            user.save()
            return redirect('browse')
    else:
        return render(request, 'main/account_activation_invalid.html')

def mentor_add_tag(request):
    if request.method == 'POST':
        form = MentorTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mentor_addtag')
    else:
        form = MentorTagForm()
    return render(request, 'main/mentor_addtag.html', {'form': form})

def mentee_add_tag(request):
    if request.method == 'POST':
        form = MenteeTagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mentee_addtag')
    else:
        form = MenteeTagForm()
    return render(request, 'main/mentee_addtag.html', {'form': form})

@login_required
def accept_mentor(request, mentor_id=None):
    mentor = CustomUser.objects.get(id=mentor_id)
    mentor.admin_approved = True
    mentor.is_active = True
    mentor.save()

    mentor = MentorProfile.objects.get(user=mentor)
    try:
        # Set a default invite by the user who has accepted the mentor
        mentee = MenteeProfile.objects.get(user=request.user)
        appointment = Appointment.objects.create(mentor = mentor, mentee = mentee)
    except MenteeProfile.DoesNotExist:
        print("Mentee profile doesn't exist for admin user accepting the invite")

    current_site = get_current_site(request)
    subject = 'You’re in! 🎉 Welcome to Cmd+J!'
    message = render_to_string('main/approved_by_admin_email.html', {
        'mentor': mentor,
    })
    to = [mentor.mentor_email]
    message.content_subtype = 'html'
    send_email_task.delay(subject, message, to)
#     to = mentor.mentor_email
#     mail.send_mail(subject, plain_message, from_email, [to], html_message=message)
    # mentor.email_user(subject, message)

    #Creating Score Table Entries for new Mentor
    for mentee in MenteeProfile.objects.filter(field_of_design=mentor.field_of_design):
        score = 0
        for t_mentee in mentee.tag.all():
            for t_mentor in mentor.tag.all():
                if(t_mentee.match_id == t_mentor.match_id):
                    score+=1
        MentorMenteeScore.objects.create(score=score,mentor=mentor,mentee=mentee)

    return redirect('admin_dashboard')


@login_required
def reject_mentor(request, mentor_id=None):
    mentor = CustomUser.objects.get(id=mentor_id)
    email = mentor.email
    mentor.delete()

    current_site = get_current_site(request)
    subject = 'You’re NOT in! 🎉 Welcome to Cmd+J!'
    message = render_to_string('main/rejected_by_admin_email.html', {
        'mentor': mentor,
    })
    to = [email]
    message.content_subtype = 'html'
    send_email_task.delay(subject, message, to)
    return redirect('admin_dashboard')


def send_request(request, mentor_id=None):
    mentor = MentorProfile.objects.get(id = mentor_id)
    mentee = MenteeProfile.objects.get(user = request.user)
    appointment = Appointment.objects.create(mentor = mentor, mentee = mentee)

    current_site = get_current_site(request)
    subject = '👋🏽 A mentee needs your guidance!'
    message = render_to_string('main/new_invitation_created_email.html', {
        'mentor': appointment.mentor,
        'mentee': appointment.mentee,
        'domain': current_site.domain,
    })
    to = [mentor.mentor_email]
    message.content_subtype = 'html'
    send_email_task.delay(subject, message, to)

    return redirect('browse')

def mentor_scheduled(request):
    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST)
        if form.is_valid():
            appointment_id = form.cleaned_data.get('appointment_id')
            print(appointment_id)
            appointment = Appointment.objects.get(id = appointment_id)
            old_datetime = appointment.datetime
            appointment.datetime = datetime.datetime.utcfromtimestamp(form.cleaned_data.get('timestamp'))
            appointment.accepted_by_mentor = True
            appointment.save()

            mentor_reminder_time = appointment.datetime - timedelta(hours=8, minutes=30)
            mentee_reminder_time = appointment.datetime - timedelta(hours=15, minutes=30)

            current_site = get_current_site(request)
            subject = 'Rain Check! ☔ - Call Rescheduled'
            message = render_to_string('main/meeting_rescheduled_email.html', {
                'mentor': appointment.mentor,
                'mentee': appointment.mentee,
                'old_date': old_datetime.strftime("%A, %d %b %Y"),
                'old_time': old_datetime.strftime("%H:%M %p"),
                'new_date': appointment.datetime.strftime("%A, %d %b %Y"),
                'new_time': appointment.datetime.strftime("%H:%M %p"),
            })
            to = [appointment.mentee.mentee_email]
            message.content_subtype = 'html'
            send_email_task.delay(subject, message, to)

            current_site = get_current_site(request)
            subject = 'Reminder for your call today!'
            message = render_to_string('main/mentee_reminder_email.html', {
                'mentor': appointment.mentor,
                'mentee': appointment.mentee,
            })
            to = [appointment.mentee.mentee_email]
            message.content_subtype = 'html'
            send_email_task.apply_async((subject, message, to), eta=mentee_reminder_time)

            current_site = get_current_site(request)
            message = render_to_string('main/mentor_reminder_email.html', {
                'mentor': appointment.mentor,
                'mentee': appointment.mentee,
            })
            to = [appointment.mentor.mentor_email]
            message.content_subtype = 'html'
            send_email_task.apply_async((subject, message, to), eta=mentor_reminder_time)
    else:
        form = AppointmentUpdateForm()

    appointments = None
    if request.user.is_mentor:
        mentor = MentorProfile.objects.get(user = request.user)
        appointments = Appointment.objects.filter(mentor = mentor, accepted_by_mentor=True)
        for appointment in appointments:
            appointment.timestamp = appointment.datetime.timestamp()
        # for app in appointments:
        #     if(app.datetime < datetime.datetime.now()):
        #         appointments.remove(app)
    return render(request, 'main/mentor_scheduled.html', {'appointments': appointments, 'form': form })

def schedule_reject(request, appointment_id):
    appointment = Appointment.objects.get(id = appointment_id)
    if appointment.mentor == request.user.mentorprofile:
        appointment.rejected_by_mentor = True
        appointment.save()
        subject = '{{mentor.mentor_first_name}} wouldn\'t be able to connect with you 😔'
        message = render_to_string('main/meeting_rejected.html', {
            'mentor': appointment.mentor,
            'mentee': appointment.mentee,
        })
        to = [appointment.mentee.mentee_email]
        message.content_subtype = 'html'
        send_email_task.delay(subject, message, to)
        appointment.delete()

    return redirect('mentor_dashboard')

@login_required
def mentor_edit_profile(request):
    mentor = MentorProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = MentorEditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            mentor.mentor_first_name = form.cleaned_data.get('first_name')
            mentor.mentor_last_name = form.cleaned_data.get('last_name')
            mentor.url = form.cleaned_data.get('url')
            mentor.social_url = form.cleaned_data.get('social_url')
            mentor.place_of_work = form.cleaned_data.get('place_of_work')
            old_field_of_design = mentor.field_of_design
            mentor.field_of_design = form.cleaned_data.get('field_of_design')
            mentor.bio = form.cleaned_data.get('bio')
            mentor.bio_updated = True
            tags = form.cleaned_data.get('tag')
            print(tags)
            old_tags = mentor.tag.all()
            if(old_tags != tags ):
                mentor.tag.clear()
                for t in tags:
                    mentor.tag.add(MentorTags.objects.get(tag=t.tag))
            mentor.save()

            #Updating Score Table if Field of Design is Updated
            if (mentor.field_of_design != old_field_of_design) or (old_tags != tags):
                MentorMenteeScore.objects.filter(mentor=mentor).delete()
                for mentee in MenteeProfile.objects.filter(field_of_design=mentor.field_of_design):
                    score = 0
                    for t_mentee in mentee.tag.all():
                        for t_mentor in mentor.tag.all():
                            if(t_mentee.match_id == t_mentor.match_id):
                                score+=1
                    MentorMenteeScore.objects.create(score=score,mentor=mentor,mentee=mentee)

            return redirect('mentor_dashboard')
    else:
        initial_data = {'first_name' : mentor.mentor_first_name,
                        'last_name' : mentor.mentor_last_name,
                        'url' : mentor.url,
                        'social_url' : mentor.social_url,
                        'place_of_work' : mentor.place_of_work,
                        'field_of_design' : mentor.field_of_design,
                        'bio' : mentor.bio,
                        'tag' : mentor.tag.all
                        }
        form = MentorEditProfileForm(instance = request.user, initial=initial_data)

    return render(request, 'main/mentor_edit_profile.html', {'form': form})

@login_required
def mentee_edit_profile(request):
    mentee = MenteeProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = MenteeEditProfileForm(request.POST, instance = request.user)
        if form.is_valid():
            form.save()
            mentee.mentee_first_name = form.cleaned_data.get('first_name')
            mentee.mentee_last_name = form.cleaned_data.get('last_name')
            mentee.url = form.cleaned_data.get('url')
            mentee.place_of_work = form.cleaned_data.get('place_of_work')
            old_field_of_design = mentee.field_of_design
            mentee.field_of_design = form.cleaned_data.get('field_of_design')
            mentee.bio = form.cleaned_data.get('bio')
            mentee.bio_updated = True
            tags = form.cleaned_data.get('tag')
            print(tags)
            old_tags = mentee.tag.all()
            if(old_tags != tags ):
                mentee.tag.clear()
                for t in tags:
                    mentee.tag.add(MenteeTags.objects.get(tag=t.tag))
            mentee.save()

            #Updating Score Table if Field of Design is Updated
            if (mentee.field_of_design != old_field_of_design) or (old_tags != tags):
                MentorMenteeScore.objects.filter(mentee=mentee).delete()
                for mentor in MentorProfile.objects.filter(field_of_design=mentee.field_of_design):
                    score = 0
                    for t_mentee in mentee.tag.all():
                        for t_mentor in mentor.tag.all():
                            if(t_mentee.match_id == t_mentor.match_id):
                                score+=1
                    MentorMenteeScore.objects.create(score=score,mentor=mentor,mentee=mentee)

            messages.success(request, 'Details Updated')
            return redirect('browse')
    else:
        initial_data = {'first_name' : mentee.mentee_first_name,
                        'last_name' : mentee.mentee_last_name,
                        'url' : mentee.url,
                        'place_of_work' : mentee.place_of_work,
                        'field_of_design' : mentee.field_of_design,
                        'bio' : mentee.bio,
                        'tag' : mentee.tag.all
                        }
        form = MenteeEditProfileForm(instance = request.user, initial=initial_data)

    return render(request, 'main/mentee_edit_profile.html', {'form': form})

@login_required
def mentor_bio_update(request):
    mentor = MentorProfile.objects.get(user = request.user)
    if request.method == 'POST':
        form = MentorBioUpdateForm(request.POST, instance = request.user)
        if form.is_valid():
            mentor.bio = form.cleaned_data.get('bio')
            mentor.bio_updated = True
            mentor.save()
            return redirect('mentor_dashboard')
    else:
        initial_data = {'bio' : mentor.bio}
        form = MentorEditProfileForm(instance = request.user, initial=initial_data)

    return render(request, 'main/mentor_bio_update.html', {'form': form})

@login_required
def mentor_opt_out(request):
    mentor = MentorProfile.objects.get(user = request.user)
    mentor.opt_out = True
    mentor.save()
    return redirect('mentor_dashboard')

@login_required
def mentor_opt_in(request):
    mentor = MentorProfile.objects.get(user = request.user)
    mentor.opt_out = False
    mentor.save()
    return redirect('mentor_dashboard')

def mentor_profile(request, mentor_name, mentor_id):
    mentor = MentorProfile.objects.get(id = mentor_id)
    booked = False
    if mentor.mentor_first_name == mentor_name :
        if request.user.is_authenticated and request.user.is_mentee:
            mentee = MenteeProfile.objects.get(user = request.user)
            booked_mentors = Appointment.objects.filter(mentee = mentee).values('mentor')
            mentor_id_list = []
            for b in booked_mentors.values():
                mentor_id_list.append(b['mentor_id'])

            if mentor.id in mentor_id_list:
                booked = True

        return render(request, 'main/mentor_profile.html', {'mentor': mentor, 'booked': booked})
    else:
        return render(request, 'main/404.html')

@login_required
def mentee_profile(request, mentee_name, mentee_id):
    mentee = MenteeProfile.objects.get(id = mentee_id)
    if mentee.mentee_first_name == mentee_name :
        return render(request, 'main/mentee_profile.html', {'mentee': mentee})
    else:
        return render(request, 'main/404.html')
