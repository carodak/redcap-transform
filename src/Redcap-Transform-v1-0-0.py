### 
# RedcapDBFormat v1.0.0, Caroline Dakoure
# carodak2@gmail.com
# TODO: 
# - Change process_csv_file to use another data structure to perform operations instead of a new panda dataframe as it's not efficient
###

from tkinter import *
from tkinter import filedialog, messagebox
import pandas as pd
import os
import sys
from datetime import datetime
from tqdm import tqdm

def open_csv_file(dir):
    file_path = filedialog.askopenfilename(initialdir=dir, filetypes=(("CSV","*.csv"), ("all files","*.*")))
    if file_path:
        df = pd.read_csv(file_path)
    else:
        print("Error: No file selected", file=sys.stderr)
    return df

# To associate suffixes with variables, my script looks at the redcap_event_name. If ever we have colomns that have no value at all, then we won't be able to associate a corresponding redcap_event name. These colomns will therefore have no suffixes.
def process_csv_file(df, redcap_events_dict, redcap_unchangeable_columns):
    new_df = pd.DataFrame(df['record_id'].drop_duplicates().reset_index(drop=True))
    column_data = {}

    progress_bar = tqdm(total=len(df.columns), desc="[ONGOING] Processing Columns")

    for col in df.columns:
        if not df[col].isnull().all() and col != 'record_id' and col != 'redcap_event_name':
            col_values = df.loc[~df[col].isnull(), ['record_id', 'redcap_event_name', col]]
            for event_name in col_values['redcap_event_name'].unique():
                event_data = col_values[col_values['redcap_event_name'] == event_name]
                event_data = event_data.set_index('record_id')[col]
                new_name = col+redcap_events_dict[event_name]
                if col in redcap_unchangeable_columns:
                    new_name = col
                event_data.name = new_name
                if event_data.name not in column_data:
                    column_data[event_data.name] = event_data
                else:
                    column_data[event_data.name] = pd.concat([column_data[event_data.name], event_data])
        elif df[col].isnull().all():
            serie  = pd.Series(name=col, index=new_df['record_id'])
            column_data[col] = serie
        progress_bar.update(1)

    progress_bar.close()

    progress_bar = tqdm(total=len(column_data), desc="[ONGOING] Merging Columns")

    for data_name, event_data in column_data.items():
        if event_data.name in new_df.columns:
            new_df[event_data.name] = new_df[event_data.name] + event_data
        else:
            new_df = new_df.merge(event_data, on='record_id', how='left')
        progress_bar.update(1)

    progress_bar.close()
    new_df.sort_values(by='record_id', inplace=True)
    return new_df


def export_to_csv(df, output_dir):
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = os.path.join(output_dir, f'redcap-transformed-{current_date}.csv')
    df.to_csv(output_filename, encoding='utf-8-sig', index=False)
    print("[COMPLETED] The operations are complete and the new .csv file has been successfully created. You can now close this program.")

def main():
    win=Tk()
    win.withdraw()
    win.geometry("700x300")

    messagebox.showinfo("File1", "Please select the csv file representing the Redcap database")
    dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    df = open_csv_file(dir)

    messagebox.showinfo("File2", "Please select the csv file representing the Redcap events correspondance (in resources folder) for your database")
    child_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    resources_dir = os.path.join(child_dir, 'resources')
    df_redcap_events = open_csv_file(resources_dir)
    redcap_events_dict = dict(zip(df_redcap_events['redcap-event'], df_redcap_events['suffix']))

    messagebox.showinfo("File3", "Please select the csv file representing the Redcap unchangeable column (in resources folder) for your database")
    df_unchangeable_columns = open_csv_file(resources_dir)
    unchangeable_columns = df_unchangeable_columns['unchangeable-columns'].tolist()

    new_df = process_csv_file(df, redcap_events_dict, unchangeable_columns)

    export_to_csv(new_df, dir)

main()