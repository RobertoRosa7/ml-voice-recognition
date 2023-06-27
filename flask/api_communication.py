import os
import requests
import time

with open(os.path.join('.env')) as envfile:
    lines = envfile.readlines()
    ASSEMBLYAI_API_KEY = lines[0].split('=')[1].replace('\n','')
    ASSEMBLYAI_URI = lines[1].split('=')[1].replace('\n','')
    

headers = {'authorization': str(ASSEMBLYAI_API_KEY), 'content-type': 'application/json'}

# upload
def get_body(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    upload_response = requests.post(url=str(ASSEMBLYAI_URI + '/upload'), headers=headers, data=read_file(filename))
    return upload_response.json()['upload_url']


# transcribe
def transcript(body):
    transcript_response = requests.post(url=str(ASSEMBLYAI_URI + '/transcript'), headers=headers, json=body)
    job_id = transcript_response.json()['id']
    return job_id


# poll
def poll(transcript_id):
    polling_response = requests.get(url=f'{ASSEMBLYAI_URI}/transcript/{transcript_id}', headers=headers)
    return polling_response.json()


def get_transcript(body):
    transcript_id = transcript(body)
    
    while True:
        data = poll(transcript_id)

        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
        
        print('Waiting for 10 seconds')
        time.sleep(10)


def save_transcript(body):
    data, error = get_transcript(body)

    if data:
        text_filenmae = os.path.join('..', 'audio_transcript', f'output-{str(time.time())}.txt')
        with open(text_filenmae, 'w') as f:
            f.write(data['text'])
            f.close()
            print("Transcription saved!!")
    else:
        raise Exception("No data found")
