from django.shortcuts import render
import cv2
import face_recognition, numpy as np
import base64
from django.http import JsonResponse
from .models import people , detection
from django.db.models import Q
from datetime import date

def index(request):
  return render(request , "index.html") 
   
def registration(request):
  return render(request, 'registration.html')

# function to perform face recognition task, if a face is recognised then returns the name of the recognised face, else reurns nothing
def face_recognition_function(unknown_encoding):
  known_encodings = []
  known_names = []
  known_people = people.objects.all()
  for person in known_people:
    encoding = np.fromstring(person.encoding[1:-1], sep=' ')
    known_encodings.append(encoding)
    known_names.append(person.name)

  matches = face_recognition.compare_faces(known_encodings, unknown_encoding, tolerance= 0.48)
  face_distance = face_recognition.face_distance(known_encodings, unknown_encoding)
  print(matches)
  if len(face_distance) > 0:
    best_match_index = np.argmin(face_distance)   
    if matches[best_match_index]:
      name = known_names[best_match_index]
      return(name)

# function to decode the base64 encoded image into a format compatible with face recognition functions
def decode_image(image_data):
  image_string = image_data.split(';base64,')[1]  
  decoded_image = np.frombuffer(base64.b64decode(image_string), np.uint8)
  frame = cv2.imdecode(decoded_image, cv2.IMREAD_COLOR)
  RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  return(RGB_frame)   

# function used to process frames to check whether face is recognised or not
def process_frame(request):
  if request.method == "POST":
    image_data = request.POST.get('image_data')
    # decode base64 image to rbg frame 
    RGB_frame = decode_image(image_data)
    # create encoding of unknown face
    face_encodings = face_recognition.face_encodings(RGB_frame)
      
    for face_encoding in face_encodings:
      # from unknown face encoding, check whether the face matches or not, if not then nothing will be returned
      name = face_recognition_function(face_encoding)
      if name:
        # before adding recognised face name to list, check whether it already exists in the list and on the same date 
        if not detection.objects.filter(Q(name=name)&Q(date=date.today())).exists():
            detection.objects.create(name=name)
            return JsonResponse({'status' : "success"})           
        return JsonResponse({'status': "unchanged"})  
                   
  return JsonResponse({"error" : "Something went wrong"})

# function to handle new user registration to database
def submit_form(request):
  if request.method == "POST":  
    name = request.POST.get('name')
    # check whether the name already exists in the database
    if people.objects.filter(name=name).exists():
      return JsonResponse ({'status':"401"})

    image_data = request.POST.get('image_data')
    RGB_frame = decode_image(image_data)
    image_encodings = face_recognition.face_encodings(RGB_frame)

    # check whether more than 1 face is present in the captured frame 
    if(len(image_encodings) > 1):
      return JsonResponse({'status':'402'})

    if image_encodings:
      image_encoding = image_encodings[0]
      # check whether the face matches with an already registered face 
      name_known = face_recognition_function(image_encoding)
      if name_known:
        response_data = {
          'status':'400',
          'name' : name_known,
        }
        return JsonResponse(response_data)
      # Convert encoding to string and save to database
      encoding_str = np.array2string(image_encoding)
      people.objects.create(encoding=encoding_str, name=name)
      return JsonResponse({'status': '201'})
    else:
      return JsonResponse({'status': 'no_face_found'})
  
  return JsonResponse({'status': 'invalid_request'})

def get_detections(request):
  draw = int(request.GET.get('draw',1))
  start = int(request.GET.get('start',0))
  length = int(request.GET.get('length',10))
  search_value = request.GET.get('search[value]','')

  data=[]
  totalRecords = 0
  filteredRecords = 0

  # counting total records in the database
  totalRecords = detection.objects.count()

  # searching operation
  if search_value:
    queryset = detection.objects.filter(Q(name__icontains=search_value)|Q(date__icontains=search_value)|Q(time__icontains=search_value))
  else:
    queryset = detection.objects.all()
  # counting total filtered records
  filteredRecords = queryset.count()

  # sorting operation
  column_index = int(request.GET.get('order[0][column]',0))
  direction = request.GET.get('order[0][dir]','asc')
  # assigning the column name to the index
  column_name = ['name','date','time'][column_index]
  # reversing the order if direction is descending
  if direction == 'desc':
    column_name = f'-{column_name}'
  queryset = queryset.order_by(column_name)

  # pagination operation
  queryset = queryset[start:start+length]

  # preparing data to be sent back to the client side in form of list 
  for entry in queryset:
    formatted_date = entry.date.strftime("%d/%m/%y")
    formatted_time = entry.time.strftime("%I:%M:%S %p")
    data.append([entry.name, formatted_date, formatted_time])

  response = {
    'draw': draw,
    'recordsTotal': totalRecords,
    'recordsFiltered': filteredRecords,
    'data':data
  }
  return JsonResponse (response)