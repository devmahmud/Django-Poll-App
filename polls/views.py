from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import Poll, Choice, Vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings  # To access your email settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from django.conf import settings


@login_required()
@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        data = json.loads(request.body)
        message = data.get("message", "")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Respond to the following: {message}, and return only plain text. Avoid any code formatting or backticks.",
                }
            ],
        )
        reply = response.choices[0].message.content
        return JsonResponse({"reply": reply})


@login_required()
def chat_page(request):
    return render(request, "polls/chat.html")


@login_required()
def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = ""
    if "name" in request.GET:
        all_polls = all_polls.order_by("text")

    if "date" in request.GET:
        all_polls = all_polls.order_by("pub_date")

    if "vote" in request.GET:
        all_polls = all_polls.annotate(Count("vote")).order_by("vote__count")

    if "search" in request.GET:
        search_term = request.GET["search"]
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)  # Show 6 contacts per page
    page = request.GET.get("page")
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop("page", True) and get_dict_copy.urlencode()

    context = {
        "polls": polls,
        "params": params,
        "search_term": search_term,
    }
    return render(request, "polls/polls_list.html", context)


@login_required()
def dashboard(request):
    polls = Poll.objects.all()
    poll_data = []

    for poll in polls:
        unique_voters = Vote.objects.filter(poll=poll).values("user").distinct().count()
        poll_data.append({"question": poll.text, "unique_voters": unique_voters})

    context = {"poll_data": poll_data}
    return render(request, "polls/dashboard.html", context)


@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)  # Show 7 contacts per page

    page = request.GET.get("page")
    polls = paginator.get_page(page)

    context = {
        "polls": polls,
    }
    return render(request, "polls/polls_list.html", context)


@login_required()
def polls_add(request):
    if request.user.has_perm("polls.add_poll"):
        if request.method == "POST":
            form = PollAddForm(request.POST)
            if form.is_valid:
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                Choice(poll=poll, choice_text=form.cleaned_data["choice1"]).save()
                Choice(poll=poll, choice_text=form.cleaned_data["choice2"]).save()

                messages.success(
                    request,
                    "Poll & Choices added successfully.",
                    extra_tags="alert alert-success alert-dismissible fade show",
                )

                return redirect("polls:list")
        else:
            form = PollAddForm()
        context = {
            "form": form,
        }
        return render(request, "polls/add_poll.html", context)
    else:
        return HttpResponse("Sorry but you don't have permission to do that!")


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")

    if request.method == "POST":
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(
                request,
                "Poll Updated successfully.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("polls:list")

    else:
        form = EditPollForm(instance=poll)

    return render(request, "polls/poll_edit.html", {"form": form, "poll": poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")
    poll.delete()
    messages.success(
        request,
        "Poll Deleted successfully.",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("polls:list")


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")

    if request.method == "POST":
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request,
                "Choice added successfully.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("polls:edit", poll.id)
    else:
        form = ChoiceAddForm()
    context = {
        "form": form,
    }
    return render(request, "polls/add_choice.html", context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect("home")

    if request.method == "POST":
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request,
                "Choice Updated successfully.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("polls:edit", poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        "form": form,
        "edit_choice": True,
        "choice": choice,
    }
    return render(request, "polls/add_choice.html", context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect("home")
    choice.delete()
    messages.success(
        request,
        "Choice Deleted successfully.",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("polls:edit", poll.id)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, "polls/poll_result.html", {"poll": poll})
    loop_count = poll.choice_set.count()
    context = {
        "poll": poll,
        "loop_time": range(0, loop_count),
    }
    return render(request, "polls/poll_detail.html", context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get("choice")
    if not poll.user_can_vote(request.user):
        messages.error(
            request,
            "You already voted this poll!",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("polls:list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()

        # get poll creator email
        poll_creator_email = poll.owner.email
        # Construct the email
        subject = f"New vote for your poll: {poll.text}"
        message = f'A new vote has been cast for your poll "{poll.text}".'
        # Send the email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [poll_creator_email])

        return render(request, "polls/poll_result.html", {"poll": poll})
    else:
        messages.error(
            request,
            "No choice selected!",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("polls:detail", poll_id)
    return render(request, "polls/poll_result.html", {"poll": poll})


@login_required
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect("home")

    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, "polls/poll_result.html", {"poll": poll})
    else:
        return render(request, "polls/poll_result.html", {"poll": poll})
