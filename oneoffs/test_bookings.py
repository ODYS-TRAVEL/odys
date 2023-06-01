import csv
import requests
from datetime import datetime

worldia_token = ''
voyageurs_token = ''
url = 'http://localhost:8002/api/v1/bookings/'

def parse_date(date_str):
    print(date_str)
    date = datetime.strptime(date_str.strip(), '%d/%m/%Y')
    date = date_str.split('/')
    # print(date)
    parsed = f'{date[2].strip()}-{date[1].strip()}-{date[0].strip()}'
    print(parsed)
    return parsed


def main():
    csv_file = open('test_bookings.csv', 'r')
    reader = csv.DictReader(csv_file)

    bookings = []
    errors = []
    completed = []
    rows = [r for r in reader]
    for row in rows[1:]:
        participants_info = row['Participants '].split('\n')
        participants = []
        broken = False
        for p in participants_info:
            detail = p.split(',')
            # print('Detail ', detail)
            # if 'SARLES' in detail[0]:
            #     broken = True
            #     continue
            date = parse_date(detail[2])
            participants.append({
                'surname': detail[0].strip(),
                'last_name': detail[1].strip(),
                'birthday': date,
            })
        # if broken:
        #     continue
        data = {
            "participants": participants,
            "client": {
                "client_id": row['Client_ID'],
                "client_profile": row['Client_Profile'],
                "dmc": "recFRCXOPwTSFEuSt",  # all are the same "Mexikoo"
                "surname": row['Client_Name'],
                "last_name": row['Client_Last_Name'],
                "country": row['Client_Country'],
                "phone": row['Client_Phone'],
                "email": "juliomenaya@gmail.com"
            },
            "agency_booking_id": row['booking_id'],
            "client_product_title_edit": row['product_name'],
            "start_date": parse_date(row['Start_Date']),
            "end_date": parse_date(row['End_Date']),
            "departure_time_edit": ':'.join(row['Departure_time'].split(':')[:2]),
            "client_hotel": row['Client_Hotel'],
            "meeting_point_edit": row['Meeting_Point'],
            "arrival_point": row['Arrival_Point'],
            "booking_details": row['Booking_Details'],
            "pax": int(row['Pax']),
            "booking_options": row['Options'],
            "agent_emails": [row["Agent's email"]]
        }
        bookings.append(data)
        token = None
        if 'worldia' in row['Agency_Id'].lower():
            token = worldia_token
        elif 'voyageurs' in row['Agency_Id'].lower():
            token = voyageurs_token
        assert token
        headers = {
            'Authorization': f'Token {token}'
        }
        response = requests.post(url, json=data, headers=headers)
        if response.status_code != 200:
            print(response.text)
            print('*' * 30)
            # print('Data error ', data)
            errors.append(data)
        if response.status_code == 200:
            completed.append(response.json())
    return bookings, completed, errors
