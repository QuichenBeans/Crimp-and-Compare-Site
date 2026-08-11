"""
URL configuration for crimpcomparesite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shoes import views
from django.views.generic import TemplateView

app_name = 'shoes'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.ShoeListView.as_view(), name='home'),

    # Search results
    path('search_results/', views.SearchResultView.as_view(), name='search_results'),

     # Shoe details
    path('shoe/<slug:slug>/', views.ShoeDetailView.as_view(), name='shoe_detail'),

    # Deals
    path('deals/', views.ShoeDealsView.as_view(), name='deals'),

    # Contact
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact_success', TemplateView.as_view(template_name='shoes/contact_success.html'), name='contact_success'),

    # Disclaimer
    path('disclaimer', views.DisclaimerView.as_view(), name='disclaimer'),

    # Blog
    path('blog/', views.ShoeBlogView.as_view(), name='blog'),

    # Guides
    path('guides/', views.ShoeGuidesView.as_view(), name='guides'),
    path('guides/<slug:slug>', views.ShoeGuideDetailView.as_view(), name='guides_detail'),

    # Dictionary
    path('dictionary/', views.ShoeDictionaryView.as_view(), name='dictionary'),

    # Categories
    path('categories/', views.ShoeCategoriesView.as_view(), name='categories'),
    path('category/<slug:slug>', views.ShoeCategoryDetailView.as_view(), name='category_detail'),

    # Quiz
    path('quiz/', views.AIQuizView.as_view(), name='quiz'),
    path('quiz/quiz_results', views.AIQuizResultsView.as_view(), name='quiz_results'),
]
