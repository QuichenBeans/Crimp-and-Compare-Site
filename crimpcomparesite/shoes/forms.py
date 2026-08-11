from django import forms

class ClimbingShoeQuizForm(forms.Form):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner (still learning basics)'),
        ('intermediate', 'Intermediate (leading 5.10 / V3-V4)'),
        ('advanced', 'Advanced (leading 5.11+ / V5+)'),
    ]
    
    CLIMBING_TYPE_CHOICES = [
        ('gym', 'Gym climbing only'),
        ('bouldering', 'Bouldering (indoor or outdoor)'),
        ('sport', 'Sport climbing (bolted routes)'),
        ('trad', 'Trad / multi-pitch'),
        ('all-around', 'All-around / mixed'),
    ]
    
    FOOT_SHAPE_CHOICES = [
        ('narrow', 'Narrow (shoes often feel too wide)'),
        ('medium', 'Medium (most shoes fit okay)'),
        ('wide', 'Wide (shoes often feel too tight)'),
    ]
    
    BUDGET_CHOICES = [
        ('under100', 'Under £100'),
        ('100-150', '£100 - £150'),
        ('150-200', '£150 - £200'),
        ('200+', '£200+'),
    ]
    
    PRIORITY_CHOICES = [
        ('comfort', 'Comfort (all-day wear)'),
        ('performance', 'Performance (max edging/hooking)'),
        ('durability', 'Durability (last as long as possible)'),
        ('value', 'Best value for money'),
    ]
    
    level = forms.ChoiceField(
        choices=LEVEL_CHOICES, 
        widget=forms.RadioSelect,
        label="What's your climbing level?"
    )
    climbing_type = forms.ChoiceField(
        choices=CLIMBING_TYPE_CHOICES, 
        widget=forms.RadioSelect,
        label="What type of climbing do you do most?"
    )
    foot_shape = forms.ChoiceField(
        choices=FOOT_SHAPE_CHOICES, 
        widget=forms.RadioSelect,
        label="How would you describe your foot shape?"
    )
    budget = forms.ChoiceField(
        choices=BUDGET_CHOICES, 
        widget=forms.RadioSelect,
        label="What's your budget?"
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES, 
        widget=forms.RadioSelect,
        label="What's your top priority?"
    )
    

class ContactForm(forms.Form):
    full_name = forms.CharField(
        max_length=200,
        label='Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Name',
            'class': 'form-control'
        })
    )
    email = forms.CharField(
        max_length=200,
        label='Email',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Email',
            'class': 'form-control'
        })
    )
    subject = forms.CharField(
        max_length=200,
        label='Subject',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Subject',
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        max_length=1000,
        label='Message',
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Message',
            'class': 'form-control'
        })
    )