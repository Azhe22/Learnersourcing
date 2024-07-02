import json
import gemini
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
from .models import WorkedOutExample, SolutionSteps, DataColumn, DataTable, Profile, Review, \
    ReviewSolutionSteps
import time

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
        'completed_workouts': WorkedOutExample.objects.filter(creator=request.user.profile, submitted=True),
        'incomplete_workouts': WorkedOutExample.objects.filter(creator=request.user.profile, submitted=False),
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
    profile = Profile.objects.get(user=request.user)
    example_list = WorkedOutExample.objects.filter(reviews__reviewer=profile).distinct()
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
    example = WorkedOutExample.objects.get(pk=example_id)
    review, created = Review.objects.get_or_create(example=example, reviewer=request.user.profile)

    if request.method == 'POST':
        # Process the review submission
        action = request.POST.get('action', '')
        if action == 'Cancel and Exit':
            # Handle cancel action
            return redirect('index')  # Redirect to wherever appropriate
        

        # Save the solution steps
        for question in example.questions.all():
            review_step_response = ReviewSolutionSteps.objects.get(review=review, question=question)
            solution_text = request.POST.get(f'solution_{question.id}', '')
            review_step_response.review_sql_statement = solution_text
            review_step_response.save()

        review.how_much_do_you_like_example = request.POST.get('like_question', '')
        review.constructive_suggestions = request.POST.get('suggestions_question', '')
        #review.how_likely_are_you_to_recommend_example = request.POST.get('recommend_question', '') #Change to slider scale
        #review.appropriateness_class = request.POST.get('appropriate_question', '')
        review.save()
        
        if action == 'Save and Exit':
            # Handle save and exit action
            return redirect('review_menu')  # Redirect to wherever appropriate    

        if action == 'Save and Submit':
            # Handle save and submit action
            # Assuming you want to redirect to a success page after submission
            return redirect('review_menu')
    # Fetch the example first (optional: add error handling if example does not exist)
    # example = get_object_or_404(Example, pk=example_id)
    review_step_responses = ReviewSolutionSteps.objects.filter(review=review)
    a = (example.data_tables.all())
    dic = {}
    for t in a:
        dic[t.name] = []
        for column in t.columns.all():
            l = {column.name: column.data_type}
            dic[t.name].append(l)
    tables = gemini.generate_table_content(example.problem_context, dic)
    time.sleep(5)
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
        'tables': tables,
        'table_lengths': {table_name: len(next(iter(columns[0].values()))) for table_name, columns in tables.items()},
        'example_id': example_id
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
        example = WorkedOutExample.objects.create(
            creator=profile,
            title=request.POST.get('topic', ''),
            problem_description=request.POST.get('problem_description', ''),
            problem_context=request.POST.get('problem_context', ''),
            submitted=True
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
        eligible_users = all_users.exclude(questions_assigned=3)
        eligible_users = eligible_users.exclude(id=profile.id)
        if eligible_users.exists():
            selected_user = random.choice(eligible_users)

            selected_user.questions_assigned = selected_user.questions_assigned + 1
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
            question = SolutionSteps.objects.create(
                example=example,
                order=steps['Step_Number'],
                text=steps['Step_Description'],
                sql_statement=steps['Suggested_Codes'],
            )
            ReviewSolutionSteps.objects.create(
                review=review,
                question=question,
                
            )

        # Handling review data


        return redirect('expert')

    # GET request: Provide initial context for form
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Create a new worked-out example', 'url': 'new_workout'},
        ]
    }
    return render(request, 'myapp/Create a new worked-out example.html', context)

@login_required(login_url='index')
def instr(request):
    temperature, description = get_weather()
    example_list = WorkedOutExample.objects.filter()
    review_list = Review.objects.filter()
    context = {
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be an Reviewer', 'url': 'review'},
        ],
        "temperature": temperature,
        "description": description,
        "example_list": example_list,
        "review_list": review_list,
    }
    return render(request, 'myapp/instructor_review_index.html', context)


@login_required(login_url='index')
def instr_review(request, example_id):
    example = WorkedOutExample.objects.get(pk=example_id)
    review, created = Review.objects.get_or_create(example=example, reviewer=request.user.profile)

    if request.method == 'POST':
        # Process the review submission
        action = request.POST.get('action', '')
        if action == 'Cancel and Exit':
            # Handle cancel action
            return redirect('index')  # Redirect to wherever appropriate
        
        if action == 'Save and Exit':
            # Handle save and exit action
            return redirect('index')  # Redirect to wherever appropriate    

        if action == 'Save and Submit':
            # Handle save and submit action
            # Assuming you want to redirect to a success page after submission
            return redirect('index')
    # Fetch the example first (optional: add error handling if example does not exist)
    # example = get_object_or_404(Example, pk=example_id)
    dic = {}
    dic["Problem Context"] = [example.problem_context]
    dic["Problem Description"] = [example.problem_description]

    count = 1
    for question in example.questions.all():
        dic["Step " + str(count)] = [question.text, question.sql_statement]
        count += 1

    for key in dic:
        dic[key] = json.dumps(dic[key])

    context = {
        'user': request.user,
        'navigation_items': [
            {'name': 'Home', 'url': 'index'},
            {'name': 'Be a Reviewer', 'url': 'review'},
            # Assuming you have a separate view or page for becoming a reviewer
            {'name': 'Conduct a Review', 'url': 'review_example', 'example_id': example_id},
            # Assuming you need to pass parameters for clarity
        ],
        'review': review,
        "example": example,
        "dic": dic,
    }
    return render(request, 'myapp/instructor_review.html', context)



