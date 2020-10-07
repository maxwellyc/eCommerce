import pandas as pd
import time, datetime, os
import np

def main():

    ################################################################################

    # read data from S3 ############################################################
    # for mini batches need to change this section into dynamical
    region = 'us-east-2'
    bucket = 'maxwell-insight'
    key = '2019-Oct.csv'
    key = 'sample.csv'
    s3file = f's3a://{bucket}/{key}'
    # read csv file on s3 into spark dataframe
    df = pd.read_csv(s3file)
    ################################################################################

    # compress time, 60 second -> 1 second
    t_step = 60 # unit in seconds, timestamp will be grouped in steps with stepsize of t_step seconds
    df['event_time'] = ((pd.to_datetime(df['event_time']) - pd.Timestamp("1970-01-01") )  / pd.Timedelta('1s'))
    t_min = df['event_time'].min()
    df['event_time'] = df['event_time'] - t_min
    df['event_time'] = df['event_time'] // t_step
    df['event_time'] = (df['event_time'] + t_min).astype(np.int64)
    df['event_time'] = pd.to_datetime(df['event_time'], unit='s', origin='unix')
    print (df.head(100))


if __name__ == "__main__":
    main()
