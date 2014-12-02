from datetime import datetime

def convert_to_british_date_format(value):
    '''Given a date in "%Y/%m/%d" display as day first '%d/%m/%Y' '''
    try:
        date_object = datetime.strptime(value, "%Y/%m/%d").date()
        return date_object.strftime('%d/%m/%Y')
    except ValueError:
        return value
