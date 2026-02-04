#partially working - 1st eval
import datetime  # for early bird offer and velocity - demand based pricing 

master_list = []
def register_event(name,date,rows,cols,base_price,revenue=0):
    event = {}
    event['name'] =name
    event['date'] =date
    event['seating'] =[[0 for _ in range(cols)] for _ in range(rows)]
    event['base_price'] =base_price
    event['revenue'] =revenue
    print(f"Event '{name}' on {date} registered,seating {rows}x{cols}.")
    master_list.append(event)

def seat_availability_normal(name,row,col):
    flag=0
    for event in master_list:
        if event['name'] ==name:
            seating = event['seating']
            if 0 <= row <len(seating) and 0 <=col <len(seating[0]):
                status =seating[row][col]
                if status == 0:
                    flag=1
                    print(f"Seat ({row}, {col}) available.")
                else:
                    print(f"Seat ({row}, {col}) booked.")
                return flag
            else:
                flag=0
                print("Invalid seat coordinates.")
                return flag
        else:
            print("invalid event")
    print("Event not found.")

def seat_availability_vip(name,row,col):
    flag=0
    for event in master_list:
        if event['name'] ==name:
            seating = event['seating']
            rows = len(seating)
            cols = len(seating[0])
            if 0 <= row <rows and 0 <= col <cols:
                for r in range(max(0, row-1), min(rows, row+2)):
                    for c in range(max(0, col-1), min(cols, col+2)):
                        if seating[r][c] == 1:
                            print(f"Seat ({row}, {col}) or surrounding seats are booked.")
                            return flag
                flag=1
                print(f"Seat ({row}, {col}) and booked in VIP mode")
                return flag
            else:
                flag=0
                print("Invalid seat coordinates.")
                return flag
    print("Event not found.")
    return flag

def book_seat_normal(name,row,col):
    for event in master_list:
        if event['name'] ==name:
            seating =event['seating']
            if 0 <= row < len(seating) and 0 <= col <len(seating[0]):
                if seat_availability_normal(name,row,col)==1: #0 in matrix
                    seating[row][col] = 1
                    event['revenue'] += calc_price(name,row,col,datetime.datetime.now().strftime("%Y-%m-%d"))
                    print("pay : ",calc_price(name,row,col,datetime.datetime.now().strftime("%Y-%m-%d")))
                    print(f"Seat ({row}, {col}) successfully booked for '{name}'.")
                else:
                    print(f"Seat ({row}, {col}) is already booked.")
                return
            else:
                print("Invalid seat coordinates.")
                return
    print("Event not found.")

def book_seat_vip(name,row,col):    
    for event in master_list:
        if event['name'] ==name:
            seating =event['seating']
            rows =len(seating)
            cols =len(seating[0])
            if 0 <= row < rows and 0 <= col < cols:
                if seat_availability_vip(name,row,col)==1:
                    for r in range(max(0, row-1), min(rows, row+2)):
                        for c in range(max(0, col-1), min(cols, col+2)):
                            seating[r][c] = 1
                    event['revenue'] += calc_price(name,row,col,datetime.datetime.now().strftime("%Y-%m-%d"))
                    print("pay : ",event['revenue'])
                    print(f"Seat ({row}, {col})booked for VIP")
                else:
                    print(f"Seat ({row}, {col}) cant be booked.")
                return
            else:
                print("Invalid seat coordinates.")
                return
    print("Event not found.")

def cancel_seat(name,row,col):
    for event in master_list:
        if event['name'] == name:
            seating = event['seating']
            if 0 <=row < len(seating) and 0 <=col <len(seating[0]):
                if seating[row][col] == 1:
                    event['revenue'] -= event['base_price']
                    seating[row][col] = 0
                    print(f"Seat ({row}, {col}) booking cancelled for '{name}'.")
                else:
                    print(f"Seat ({row}, {col}) is not booked.")
                return
            else:
                print("Invalid seat coordinates.")
                return
    print("Event not found.")

def cancel_event(name):
    for event in master_list:
        if event['name'] == name:
            master_list.remove(event)
            print(f"Event" ,name, "cancelled.")
            return
    print("Event not found.")
 
def calc_price(name,row,col,booking_date):
    for event in master_list:
        if event['name'] == name:
            seating = event['seating']
            if 0 <= row < len(seating) and 0 <= col < len(seating[0]):
                base_price =event['base_price']
                rows =len(seating)
                inc_per_row =(0.4 * base_price) / rows   #have to do the range of prices for each row to make price corner < center
                row_price =base_price + (row * inc_per_row)
                event_dt =datetime.datetime.strptime(event['date'], "%Y-%m-%d")
                bbook_dt =datetime.datetime.strptime(booking_date, "%Y-%m-%d")
                days_togo =(event_dt - bbook_dt).days
                if days_togo>0:
                    eb_discount = min(0.5 * base_price, (0.5 * base_price) / days_togo) 
                else:
                    eb_discount =0
                final_price = row_price -eb_discount
                print(f"Seat ({row}, {col}) price for event '{name}' is: {final_price:.2f}")
                return final_price
            else:
                print("Invalid seat coordinates.")
                return None
    print("Event not found.")
    return None

#menu driven with create and delete event , do and cancel booking,view availability
choice =0
while choice !=6:
    print("1. create an event\n2. book a ticket\n3. withdraw a ticket\n4. delete an event\n5. view seat availability\n6.break")
    if choice==1:
        name=input("Movie name: ")




