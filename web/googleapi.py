import sys
import io
import os
import datetime
from django.conf import settings
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types
from google.cloud import storage

# global variable, please change them with your values
bucket_name = "erguwhsd"
output_file = "output.txt"


def upload_file_to_cloud_storage(audio_file):
    bucket_url = "gs://{}/{}".format(bucket_name, audio_file)
    file_name = os.path.join(settings.MEDIA_ROOT, audio_file)
    print("file_name:" + file_name)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(audio_file)
    print("bucket_url:" + bucket_url)
    print(u"{} is uploading to storage...".format(bucket_url))
    blob.upload_from_filename(file_name)
    print("File is uploaded.")
    return bucket_url


def convert_speech_to_text(bucket_file_url, speaker_count, output_file="output.txt"):
    client = speech.SpeechClient()

    audio = {"uri": bucket_file_url}
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        enable_speaker_diarization=True,
        diarization_speaker_count=speaker_count,
        model="phone_call",
        enable_word_time_offsets=True,
        use_enhanced=True,
        enable_automatic_punctuation=True,
        language_code="en-US")

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for speech-to-text operation to complete...")
    response = operation.result()

    with open(output_file, "w") as text_file:
        for result in response.results:
            alternative = result.alternatives[0]
            current_speaker_tag = -1
            transcript = ""
            time = 0
            for word in alternative.words:
                if word.speaker_tag != current_speaker_tag:
                    if (transcript != ""):
                        print(u"Speaker {} - {} - {}".format(current_speaker_tag, str(datetime.timedelta(seconds=time)),
                                                             transcript), file=text_file)
                    transcript = ""
                    current_speaker_tag = word.speaker_tag
                    time = word.start_time.seconds

                transcript = transcript + " " + word.word
        if transcript != "":
            print(
                u"Speaker {} - {} - {}".format(current_speaker_tag, str(datetime.timedelta(seconds=time)), transcript),
                file=text_file)
        print(u"Speech to text operation is completed, output file is created: {}".format(output_file))
        return output_file


def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

if __name__ == '__main__':
    globals()[sys.argv[1]](sys.argv[2])
