from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, MentorTags, MenteeTags, Appointment, MentorProfile

DESIGN_FIELD=[
    ('UX Design','UX Design'),
    ('Graphic Design','Graphic Design'),
    ('Animation & Motion Graphics','Animation & Motion Graphics'),
    ('Film & Videography','Film & Videography'),
    ('Industrial Design','Industrial Design'),
    ('Fashion & Textiles','Fashion & Textiles'),
]

MENTEE_QUESTIONS=[
    ('q1','What would you try if it was okay to fail?'),
    ('q2','What inspired you to take up design?'),
    ('q3','My design guilty pleasure is...'),
    ('q4','A social cause I care about...'),
    ('q5','I nerd out about...'),
    ('q6','This year I really want to...'),
]

MENTEE_QUESTIONS_DICT={
    'q1':'What would you try if it was okay to fail?',
    'q2':'What inspired you to take up design?',
    'q3':'My design guilty pleasure is...',
    'q4':'A social cause I care about...',
    'q5':'I nerd out about...',
    'q6':'This year I really want to...',
}

class MentorSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username=None
    email = forms.EmailField(max_length=254, required=True)
    url = forms.URLField(required=True)
    social_url = forms.URLField(required=False) 
    place_of_work = forms.CharField(max_length=200,required=True)
    field_of_design = forms.CharField(max_length=100,widget=forms.Select(choices=DESIGN_FIELD), required=True)
    tag = forms.ModelMultipleChoiceField(
        queryset=MentorTags.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class':'ks-cboxtags'}),
        required=False,
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2','field_of_design','place_of_work','url','social_url','tag', )

class MenteeSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    username=None
    email = forms.EmailField(max_length=254, required=True)
    url = forms.URLField(required=True) 
    place_of_work = forms.CharField(max_length=100, required=True)
    field_of_design = forms.CharField(max_length=100,widget=forms.Select(choices=DESIGN_FIELD), required=True)
    question1 = forms.CharField(max_length=100,widget=forms.Select(choices=MENTEE_QUESTIONS), required=True)
    question1_answer = forms.CharField(max_length=500,required=True, widget=forms.Textarea(attrs={'rows':5}))
    question2 = forms.CharField(max_length=100,widget=forms.Select(choices=MENTEE_QUESTIONS), required=True)
    question2_answer = forms.CharField(max_length=500,required=True, widget=forms.Textarea(attrs={'rows':5}))
    question3 = forms.CharField(max_length=100,widget=forms.Select(choices=MENTEE_QUESTIONS), required=True)
    question3_answer = forms.CharField(max_length=500,required=True, widget=forms.Textarea(attrs={'rows':5}))
    bio = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows':5}))
    tag = forms.ModelMultipleChoiceField(
        queryset=MenteeTags.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2','field_of_design','place_of_work','url','bio','question1','question1_answer','question2','question2_answer','question3','question3_answer', )

class MentorTagForm(forms.ModelForm):
    tag = forms.CharField(max_length=30, required=True)
    tag_auto_bio = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = MentorTags
        fields = ('tag',)

class MenteeTagForm(forms.ModelForm):
    tag = forms.CharField(max_length=30, required=True)

    class Meta:
        model = MenteeTags
        fields = ('tag',)

class AppointmentUpdateForm(forms.ModelForm):
    appointment_id = forms.IntegerField(required = True)
    timestamp = forms.IntegerField(
        required = False,
        widget=forms.DateTimeInput(attrs={
            'class': '',
            'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Appointment
        fields = ('appointment_id','timestamp',)

class MentorEditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    url = forms.URLField(max_length=200, required=True)
    social_url = forms.URLField(required=False) 
    place_of_work = forms.CharField(max_length=100, required=True)
    field_of_design = forms.CharField(max_length=100,widget=forms.Select(choices=DESIGN_FIELD), required=True)
    bio = forms.CharField(max_length=500, widget=forms.Textarea, required=True)
    tag = forms.ModelMultipleChoiceField(
        queryset=MentorTags.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','field_of_design','place_of_work','url','social_url','bio', 'tag', )

class MenteeEditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    url = forms.URLField(max_length=200) 
    place_of_work = forms.CharField(max_length=100)
    field_of_design = forms.CharField(max_length=100,widget=forms.Select(choices=DESIGN_FIELD))
    bio = forms.CharField(max_length=500, widget=forms.Textarea)
    tag = forms.ModelMultipleChoiceField(
        queryset=MenteeTags.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name','field_of_design','place_of_work','url','bio', 'tag', )

class MentorBioUpdateForm(forms.ModelForm):
    bio = forms.CharField(max_length=500, widget=forms.Textarea)

    class Meta:
        model=MentorProfile
        fields = ('bio',)
