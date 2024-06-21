import json
#import gemini
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.db.models import F
import random
from .models import Example, ReviewQuestion, Question, DataColumn, DataTable, Profile, Review, ReviewQuestionResponse, \
    ReviewStepResponse


def get_weather():
    api_key = "439d4b804bc8187953eb36d2a8c26a02"
    base_url = "https://openweathermap.org/data/2.5/weather?id=4928096"
    url = f"{base_url}&appid={api_key}"
    response = requests.get(url)
    # Parse JSON response
    if response.status_code == 200:
        weather_data = json.loads(response.content)
        return weather_data['main']['temp'], weather_data['weather'][0]['description']
    return None, None


# Create your views here.
@csrf_protect
def index(request):
    context = {'user': request.user}
    if request.method == 'GET' and 'next' in request.GET:
        messages.info(request, 'Please log in to access that page.')
    if request.method == "POST":
        if 'sign_in' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # More specific redirection after login
            else:
                messages.error(request, 'Invalid username or password.')
        elif 'sign_up' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            # Additional error handling for existing users
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                Profile.objects.create(user=user)
                return redirect('index')
    context['sign_in_visibility'] = 'hidden' if request.user.is_authenticated else 'visible'
    return render(request, 'myapp/home.html', context)


def sign_in(request):
    return render(request, 'myapp/sign_in.html', {})


def logout_view(request):
    logout(request)
    return redirect('index')


@login_required(login_url='index')
def expert(request):
    context = {'navigation_items': [
        {'name': 'Home', 'url': 'index'},
        {'name': 'Be an Expert', 'url': 'expert'},

    ],
        'completed_workouts': Example.objects.filter(creator=request.user.profile, completed=True),
        'incomplete_workouts': Example.objects.filter(creator=request.user.profile, completed=False),
    }
    return render(request, 'myapp/be_an_expert.html', context)

@login_required(login_url='index')
def explore(request):
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be an Explorer', 'url': 'explorer'},
        ]
    }
    return render(request, 'myapp/be_an_explorer.html', context)

@login_required(login_url='index')
def review_menu(request):
    temperature, description = get_weather()
    example_list = Example.objects.filter()
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be an Reviewer', 'url': 'review'},
        ],
        "temperature": temperature,
        "description": description,
        "example_list": example_list,
    }
    return render(request, 'myapp/be_a_reviewer.html', context)


@login_required(login_url='index')
def review(request, example_id):
    example = Example.objects.get(pk=example_id)
    review, created = Review.objects.get_or_create(example=example, reviewer=request.user.profile)

    if request.method == 'POST':
        # Process the review submission
        action = request.POST.get('action', '')
        if action == 'Cancel and Exit':
            # Handle cancel action
            return redirect('index')  # Redirect to wherever appropriate
        

        # Save the solution steps
        for question in example.questions.all():
            solution_text = request.POST.get(f'solution_{question.id}', '')
            ReviewStepResponse.objects.update_or_create(
                review=review, question=question,
                defaults={'sql_statement': solution_text}
            )


        if action in ['Save and Exit', 'Save and Submit']:
            review.problem_context_like = request.POST.get('problem_context_like', '')
            review.problem_context_suggestions = request.POST.get('problem_context_suggestions', '')
            review.recommendation_likelihood = request.POST.get('recommendation_likelihood', '')
            review.appropriateness_class = request.POST.get('appropriateness_class', '')
            review.save()
        
        if action == 'Save and Exit':
            # Handle save and exit action
            return redirect('index')  # Redirect to wherever appropriate    

        if action == 'Save and Submit':
            # Handle save and submit action
            # Assuming you want to redirect to a success page after submission
            return redirect('index')
    # Fetch the example first (optional: add error handling if example does not exist)
    # example = get_object_or_404(Example, pk=example_id)
    review_step_responses = ReviewStepResponse.objects.filter(review=review)

    context = {
        'user': request.user,
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be a Reviewer', 'url': 'review'},
            # Assuming you have a separate view or page for becoming a reviewer
            {'name': 'Conduct a Review', 'url': 'review_example', 'example_id': example_id},
            # Assuming you need to pass parameters for clarity
        ],
        'review_step_responses': review_step_responses,
        "example": example,
    }
    return render(request, 'myapp/Show_Review_Examples.html', context)


@login_required(login_url='index')
def new_workout(request):
    if request.method == "POST":
        # Decode the POST data
        try:
            data_tables_data = json.loads(request.POST.get('data_table_form_data', '[]'))
            step_tables_data = json.loads(request.POST.get('step_tables', '[]'))
            review_data = json.loads(request.POST.get('review', '[]'))

        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON data", status=400)

        # Retrieve the profile of the logged-in user
        profile = Profile.objects.get(user=request.user)

        # Create the Example entry
        example = Example.objects.create(
            creator=profile,
            title=request.POST.get('topic', 'No title provided'),
            project_description=request.POST.get('problem_description', ''),
            project_context=request.POST.get('problem_context', ''),
            completed=True
        )
        # Create Data Tables and Columns
        for table_info in data_tables_data:
            data_table = DataTable.objects.create(
                example=example,
                name=table_info['table_name']  # Assuming the table name is in the first position
            )
            for column_info in table_info['columns']:
                DataColumn.objects.create(
                    data_table=data_table,
                    name=column_info['Attribute_Name'],
                    data_type=column_info['Attribute_Type']
                )
        
        all_users = Profile.objects.all()
        eligible_users = all_users.exclude(questions_assigned__gte=3)
        if eligible_users.exists():
            selected_user = random.choice(eligible_users)

            selected_user.questions_assigned = F('questions_assigned') + 1
            review = Review.objects.create(
            example=example,
            reviewer=selected_user
        )
        else:
            review = Review.objects.create(
            example=example,
            reviewer=request.user.profile  # Assuming the creator is also the reviewer for now
        )
        # Create Questions from step_tables_data
        for idx, steps in enumerate(step_tables_data, start=1):
            question = Question.objects.create(
                example=example,
                order=steps['Step_Number'],
                text=steps['Step_Description'],
            )
            ReviewStepResponse.objects.create(
                review=review,
                question=question,
                sql_statement=steps['Suggested_Codes'],
            )

        # Handling review data

        for response_data in review_data:
            question = ReviewQuestion.objects.get(pk=response_data["question_id"])
            ReviewQuestionResponse.objects.create(
                review=review,
                question=question,
                rating=response_data["rating"],
            )

        return redirect('expert')

    # GET request: Provide initial context for form
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Create a new worked-out example', 'url': 'new_workout'},
        ],
        'review_questions': ReviewQuestion.objects.all(),

    }
    return render(request, 'myapp/Create a new worked-out example.html', context)
