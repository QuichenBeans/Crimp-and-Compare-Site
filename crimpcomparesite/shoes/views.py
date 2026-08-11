from django.shortcuts import render
from .models import Category, Shoe, RetailerOffer, Dictionary, Guide
from .forms import ClimbingShoeQuizForm, ContactForm
from .filters import ShoeSearch, ShoeFilter
from .utils import DeepSeekClimbingShoeClient
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django_filters.views import FilterView
from django.shortcuts import get_object_or_404
from django.db.models import Min, Max, Q, F, Prefetch, Case, When, Value, IntegerField
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.core.cache import cache
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
import json
import hashlib


# Create your views here.

# Home view
class ShoeListView(ListView):
    model = Shoe
    template_name = 'shoes/home.html'
    context_object_name = 'shoe_list'
    paginate_by = 12

    def get_queryset(self):
        return Shoe.objects.prefetch_related('offers').annotate(
            min_price=Min('offers__price'),
            max_price=Max('offers__price')
        )

class ShoeDealsView(FilterView):
    model = Shoe
    template_name = 'shoes/deals.html'
    context_object_name = 'shoes_with_deals'
    filterset_class = ShoeFilter
    paginate_by = 10

    def get_queryset(self):
        # Get shoes with at least one active deal
        shoes = Shoe.objects.filter(
            offers__discounted_price__lt=F('offers__price'),
        ).distinct()
        
        # Prefetch active deals for these shoes
        shoes = shoes.prefetch_related(
            Prefetch('offers',
                    queryset=RetailerOffer.objects.filter(
                        discounted_price__lt=F('price'),
                    ),
                    to_attr='active_deals')
        )
        
        return shoes
    
class ShoeDictionaryView(ListView):
    model = Dictionary
    template_name = 'shoes/dictionary.html'
    
    def get_queryset(self):
        return Dictionary.objects.all().order_by('heading', 'term')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        terms = self.get_queryset()

        grouped_data = []

        # This gets the values of the heading field in the db makes sure they are unique and orders them alphabetically
        unique_headings = terms.values_list('heading', flat=True).distinct().order_by('heading')

        for heading in unique_headings:
            section_terms = terms.filter(heading=heading) # This filters all terms that belong to the unique heading
            # keeps terms where example is not null (so there is an example), removes when example is an empty string and checks that a term exists
            has_example = section_terms.filter(example__isnull=False).exclude(example='').exists()
            
            grouped_data.append({
                'heading': heading,
                'terms': section_terms,
                'has_example': has_example,
            })

        context['grouped_data'] = grouped_data
        return context

class ShoeBlogView(TemplateView):
    template_name = 'shoes/blog.html'

class ShoeGuidesView(ListView):
    model = Guide
    template_name = 'shoes/guides.html'
    context_object_name = 'guides'

class ShoeGuideDetailView(DetailView):
    model = Guide
    template_name = 'shoes/guides_detail.html'
    context_object_name = 'guide_detail'

class ShoeCategoriesView(ListView):
    model = Category
    template_name = 'shoes/categories.html'
    context_object_name = 'shoe_categories'

    def get_queryset(self):
        ordered_category = Category.objects.annotate(
            category_order=Case(
                When(name='Beginner', then=Value(0)),
                When(name='Intermediate', then=Value(1)),
                When(name='Advanced', then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by('category_order')
        return ordered_category

class ShoeCategoryDetailView(ListView):
    model = Shoe
    template_name = 'shoes/category_detail.html'
    context_object_name = 'category_detail'
    paginate_by = 12

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Shoe.objects.filter(category=self.category).prefetch_related('offers').annotate(
            min_price=Min('offers__price'),
            max_price=Max('offers__price')
    )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
    

class ContactView(FormView):
    template_name = 'shoes/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        subject = f'New Contact Form Submission: {cleaned_data["subject"]}'
        message = f'''
                Contact Form Details:
                Name: {cleaned_data['full_name']}
                Email: {cleaned_data['email']}
                Subject: {cleaned_data['subject']}

                Message: {cleaned_data['message']}

                ---
                This email was sent from your website contact form
                '''
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['crimpandcompare@gmail.com']
        )
        return super().form_valid(form)

def contact_success(request):
    return render(request, 'shoes/contact_success.html')

class DisclaimerView(TemplateView):
    template_name = 'shoes/disclaimer.html'


# Shoe detail view - shows more details of a shoe
class ShoeDetailView(DetailView):
    model = Shoe
    template_name = 'shoes/shoe_detail.html'
    context_object_name = 'shoe_detail'

    def get_queryset(self):
        return Shoe.objects.prefetch_related('offers', 'category')

# Search results
class SearchResultView(FilterView):
    model = Shoe
    template_name = 'shoes/search_results.html'
    context_object_name = 'search_shoes'
    filterset_class = ShoeSearch

    def get_queryset(self):
        return Shoe.objects.prefetch_related('offers').annotate(
            min_price=Min('offers__price'),
            max_price=Max('offers__price'),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context
    

class AIQuizView(FormView):
    template_name = 'shoes/quiz_form.html'
    form_class = ClimbingShoeQuizForm
    success_url = reverse_lazy('quiz:quiz_results')

    def form_valid(self, form):
        quiz_data = {
            'level': form.cleaned_data['level'],
            'climbing_type': form.cleaned_data['climbing_type'],
            'foot_shape': form.cleaned_data['foot_shape'],
            'budget': form.cleaned_data['budget'],
            'priority': form.cleaned_data['priority'],
        }

        self.request.session['quiz_answers'] = quiz_data

        cache_key = self._get_cache_key(quiz_data)
        
        cached_result = cache.get(cache_key)
        if cached_result:
            self.request.session['structured_recommendation'] = cached_result
            self.request.session['recommendation_source'] = 'cache'
            messages.success(self.request, "Loaded recommendations from cache!")
            return super().form_valid(form)
        
        try:
            client = DeepSeekClimbingShoeClient()
            recommendation = client.get_recommendation(quiz_data)
            
            # Cache for 24 hours
            cache.set(cache_key, recommendation, 86400)
            
            # Store in session
            self.request.session['structured_recommendation'] = recommendation
            self.request.session['recommendation_source'] = 'api'
            
            messages.success(self.request, "Got your personalized recommendations!")
            
        except Exception as e:
            messages.error(self.request, f"Unable to get recommendations: {str(e)}")
            return super().form_invalid(form)
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Handle invalid form"""
        messages.error(self.request, "Please answer all questions before continuing.")
        return super().form_invalid(form)
    
    def _get_cache_key(self, quiz_data):
        """Generate unique cache key from quiz answers"""
        sorted_data = json.dumps(quiz_data, sort_keys=True)
        return f"shoe_rec_{hashlib.md5(sorted_data.encode()).hexdigest()}"


class AIQuizResultsView(TemplateView):
    pass

