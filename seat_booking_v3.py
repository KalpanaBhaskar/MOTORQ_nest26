import datetime  # for early bird offer and velocity - demand based pricing 
#coordinates follow zero based indexing
master_list = []
def register_event(name,date,rows,cols,base_price,revenue=0):
    event = {}
    event['name'] =name
    event['date'] =date
    event['seating'] =[[0 for _ in range(cols)] for _ in range(rows)]
    event['base_price'] =base_price
    event['revenue'] =revenue
    event['reg_date'] =datetime.datetime.now().strftime("%Y-%m-%d")
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
#assign codes to a user for booking and cancellation - used to verify for cancellation,dictionary - code - key, event name, vip list of tuples , normal list of tuples  - value
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
                    event['revenue'] += calc_price_vip(name,row,col,datetime.datetime.now().strftime("%Y-%m-%d"))
                    print("pay : ",calc_price_vip(name,row,col,datetime.datetime.now().strftime("%Y-%m-%d")))
                    print(f"Seat ({row}, {col})booked for VIP")
                else:
                    print(f"Seat ({row}, {col}) cant be booked.")
                return
            else:
                print("Invalid seat coordinates.")
                return
    print("Event not found.")

def cancel_seat_normal(name,row,col):
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

def cancel_seat_vip(name,row,col):
    for event in master_list:
        if event['name'] == name:
            seating = event['seating']
            rows =len(seating)
            cols =len(seating[0])
            if 0 <= row < rows and 0 <= col < cols:
                cancel = True
                for r in range(max(0, row-1), min(rows, row+2)):
                    for c in range(max(0, col-1), min(cols, col+2)):
                        if seating[r][c] == 0:
                            cancel = False
                            break
                    if not cancel:
                        break
                if cancel:
                    for r in range(max(0, row-1), min(rows, row+2)):
                        for c in range(max(0, col-1), min(cols, col+2)):
                            seating[r][c] = 0
                    event['revenue'] -= event['base_price'] * 1.5
                    print(f"Seat ({row}, {col}) VIP seat cancelled for '{name}'.")
                else:
                    print(f"Seat ({row}, {col}) cannot cancel VIP booking.")  # surrounding seats filled
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
                reg_dt =datetime.datetime.strptime(event['reg_date'], "%Y-%m-%d")
                bbook_dt =datetime.datetime.strptime(booking_date, "%Y-%m-%d")
                days_togo =(event_dt - bbook_dt).days
                if days_togo>0:
                    eb_discount = min(0.5 * base_price, (0.5 * base_price)/ max(((event_dt-reg_dt).days -days_togo),1))
                else:
                    eb_discount =0
                final_price =row_price -eb_discount
                print(f"Seat ({row}, {col}) price for '{name}' is: {final_price:.2f}")
                return final_price
            else:
                print("Invalid seat coordinates.")
                return None
    print("Event not found.")
    return None

def calc_price_vip(name,row,col,booking_date):
    for event in master_list:
        if event['name'] == name:
            seating = event['seating']
            if 0 <= row < len(seating) and 0 <= col < len(seating[0]):
                base_price =event['base_price']
                rows =len(seating)
                inc_per_row =(0.4 * base_price) / rows
                row_price =base_price + (row * inc_per_row)
                event_dt =datetime.datetime.strptime(event['date'], "%Y-%m-%d")
                bbook_dt =datetime.datetime.strptime(booking_date, "%Y-%m-%d")
                reg_dt =datetime.datetime.strptime(event['reg_date'], "%Y-%m-%d")
                days_togo =(event_dt - bbook_dt).days
                if days_togo>0:
                    eb_discount = min(0.5 * base_price, (0.5 * base_price)/max(1,((event_dt-reg_dt).days -days_togo)) )  # days so far
                else:
                    eb_discount =0
                normal_price = row_price -eb_discount
                vip_price = normal_price *1.5 #for vip using seat
                surrounding_seats =0
                rows =len(seating)
                cols =len(seating[0])
                for r in range(max(0, row-1), min(rows, row+2)):
                    for c in range(max(0, col-1), min(cols, col+2)):
                        if (r != row or c != col):
                            surrounding_seats += 1
                vip_price += normal_price * (surrounding_seats) // 2
                print(f"Seat ({row}, {col}) VIP price for event '{name}' is: {vip_price:.2f}")
                return vip_price
            else:
                print("Invalid seat coordinates.")
                return None
    print("Event not found.")
    return None

def automatic_book_seat_normal(name,num_seats):
    for event in master_list:
        if event['name'] ==name:
            seating =event['seating']
            rows =len(seating)
            cols =len(seating[0])
            available_seats =[]
            for r in range(rows,-1,-1):
                for c in range(cols):
                    if seating[r][c] ==0:
                        available_seats.append((r,c))
            if len(available_seats) < num_seats:
                print(f"Only {len(available_seats)} seats available")
                return
            #available_seats=     
            suggested_seats = available_seats[:num_seats]
            print(f"Suggested seats for '{name}': {suggested_seats}")
            confirm =input("book these seats? (yes/no): ")
            if confirm.lower() == 'yes':
                total_price =0
                for seat in suggested_seats:
                    r,c =seat
                    seating[r][c] =1
                    price =calc_price(name,r,c,datetime.datetime.now().strftime("%Y-%m-%d"))
                    total_price +=price
                event['revenue'] += total_price
                print(f"Seats {suggested_seats} successfully booked for '{name}'. Total payment: {total_price:.2f}")
            else:
                print("Booking cancelled.")
            return
    print("Event not found.")


#menu driven with create and delete event , do and cancel booking,view availability , autobooking
choice =0
while choice !=6:
    print("1. create an event\n2. book a ticket\n3. withdraw a ticket\n4. delete an event\n5. view seat availability\n6.autobook normal seats\n7.break")
    choice =int(input("enter choice: "))
    if choice==1:
        name =input("event name: ")
        date =input("event date: ")
        rows =int(input("number of rows: "))
        cols =int(input("number of columns: "))
        base_price =float(input("base price: "))
        register_event(name,date,rows,cols,base_price)
    elif choice==2:
        name =input("event name: ")
        row =int(input("row number: "))
        col =int(input("column number: "))
        mode =input("normal/vip: ")
        if mode=="normal":
            book_seat_normal(name,row,col)
        elif mode=="vip":
            book_seat_vip(name,row,col)
        else:
            print("invalid mode")
    elif choice==3:
        name =input("event name: ")
        row =int(input("row number: "))
        col =int(input("column number: "))
        mode =input("normal/vip: ")
        if mode=="normal":
            cancel_seat_normal(name,row,col)
        elif mode=="vip":
            cancel_seat_vip(name,row,col)
        
    elif choice==4:
        name =input("event name: ")
        cancel_event(name)

    elif choice==5:
        name =input("event name: ")
        row =int(input("row number: "))
        col =int(input("column number: "))
        mode =input("normal/vip: ")
        if mode=="normal":  
            seat_availability_normal(name,row,col)
        elif mode=="vip":
            seat_availability_vip(name,row,col)
    
    elif choice==6:
        name =input("event name: ")
        num_seats =int(input("number of seats to auto book: "))
        automatic_book_seat_normal(name,num_seats) 
    elif choice==7:
        break