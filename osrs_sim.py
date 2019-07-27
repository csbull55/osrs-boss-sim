import fractions as fc
import discord
import numpy as np
import pandas as pd
import droprate
from secrets import token

# defines some variables
token = token()
client = discord.Client()

# reads drop rates file
drop_rates = pd.read_csv("./drop_rates.csv")


# defines the functions for returning rates
def roll_df(boss):
    # new df for boss inputted
    df_roll = drop_rates[drop_rates['Boss'] == boss.title()]
    df_roll.reset_index(drop=True, inplace=True)

    # extracts denominator from rate
    df_roll['d_rate'] = df_roll['Rate'].apply(lambda x: fc.Fraction(x).denominator)

    # finds lcm and creates new column on # of rolls
    lcm = droprate.lcm_multi(df_roll['d_rate'])
    df_roll['rolls'] = lcm / df_roll['d_rate']
    return df_roll


def boss_lcm(boss):
    # new df for boss inputted
    df_roll = drop_rates[drop_rates['Boss'] == boss.title()]
    df_roll.reset_index(drop=True, inplace=True)

    # extracts denominator from rate
    df_roll['d_rate'] = df_roll['Rate'].apply(lambda x: fc.Fraction(x).denominator)

    # finds lcm and creates new column on # of rolls
    lcm = droprate.lcm_multi(df_roll['d_rate'])
    return lcm


# this is the boss sim, replies to messages with !boss
@client.event
async def on_message(message):
    if message.content.startswith('!boss'):

        # assigns inputs to variables
        user_input = message.content.split(' ')
        boss = user_input[1]
        kc = int(user_input[2])

        # runs functions for boss
        item_df = roll_df(boss)
        lcm = boss_lcm(boss)

        # creates an array of rolls for kc entered and boss lcm, creates empty drops array
        roll = np.random.randint(1, lcm, size=kc)
        drops = []

        # creates df for item rolls, uses above function to build
        item_key = pd.DataFrame(columns=['key', 'item'])
        i = 1
        for index, row in item_df.iterrows():
            count = int(item_df['rolls'][index])
            while count > 0:
                item_key.loc[i] = [str(i), item_df.loc[index]['Item']]
                count -= 1
                i += 1

        # checks rolls against drop table, returns item and adds to 'drops' list
        for item in item_key['key']:
            if int(item) in roll:
                drops.append((item_key['item'][int(item)]))

        # returns message based on drops
        if len(drops) == 0:
            drops_msg = "After {} kc at {}, you've received zero uniques".format(kc, boss.title())
        elif len(drops) >= 1:
            drop_lines = ("\n".join(drops))
            drops_msg = "In {} kc at {}, you've recieved the following items:\n{}".format(kc, boss.title(), drop_lines)

        # sends message with results
        channel = message.channel
        await channel.send(drops_msg)

# lets you know that the bot is ready
@client.event
async def on_ready():
    print('the bot is ready')

client.run(token)
