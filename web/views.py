from background_task import background
from django.core.files import File
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from web.googleapi import upload_file_to_cloud_storage, convert_speech_to_text
from web.forms import AudioForm, UserCreationForm
from web.models import User, Audio, Transcript

from django.conf import settings

def upload(request):
    if request.method == 'POST':
        form = AudioForm(request.POST, request.FILES)
        if form.is_valid():
            audio = form.save()
            # fix bug: TypeError: Object of type UUID is not JSON serializable
            request.session['audio_id'] = str(audio.id)
            request.session['speaker_count'] = str(audio.speaker_num)
            print("MEDIA_ROOT: "+settings.MEDIA_ROOT+" ,STATIC_ROOT: "+settings.STATIC_ROOT)
            return redirect('wait')
    else:
        form = AudioForm()
    return render(request, 'upload.html', {
        'form': form
    })


def wait(request):
    audio_id = request.session.get('audio_id')
    speaker_count = request.session.get('speaker_count')
    process(audio_id, speaker_count)
    return render(request, 'wait.html', {'audio': audio_id})


@background()
def process(audio_id, speaker_count):
    audio = Audio.objects.filter(pk=audio_id)[0]
    audio_file_bucket_url = upload_file_to_cloud_storage(audio.audio.name)
    transcript = convert_speech_to_text(audio_file_bucket_url, int(speaker_count))
    print(transcript)
    transcript_file = Transcript(audio=audio)
    with open(transcript, "r") as original_file:
        myfile = File(original_file)
        transcript_file.transcript.save(audio.audio.name.replace('mp3', 'txt'), myfile)
        transcript_file.save()


@csrf_exempt
def check_status(request):
    transcript_id = request.POST['transcript_id']
    transcript = Transcript.objects.filter(audio_id=transcript_id)
    if len(transcript) > 0:
        return JsonResponse({"completed": True, 'task_id': transcript_id, 'success_message': 'success'})
    else:
        return JsonResponse({"completed": False, 'success_message': 'failed'})


def result(request):
    task_id = request.GET.get('task_id')
    print(task_id)
    transcript_file = Transcript.objects.filter(audio_id=task_id)[0]
    return render(request, 'result.html', {'transcript': transcript_file})


class SignUpView(CreateView):
    template_name = 'signup.html'
    form_class = UserCreationForm


class UserDetail(DetailView):
    model = User
    template_name = 'user_detail.html'


def validate_username(request):
    username = request.POST.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
