import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def save_table(actions_df):
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=actions_df.values, colLabels=actions_df.columns, cellLoc='center', loc='center')
    fig.savefig("data_visual/table.png")

def save_line_chart_a(actions_df):
    # Group by Date and count occurrences of Action "A"
    actions_a = actions_df[actions_df['Action'] == 'A']
    actions_a_grouped = actions_a.groupby("Date").size()

    plt.figure(figsize=(8, 4))
    plt.plot(actions_a_grouped.index, actions_a_grouped.values, marker="o", color="green")
    plt.title("Line Chart for Action A")
    plt.xlabel("Date")
    plt.ylabel("Count of Action A")
    plt.xticks(rotation=45)
    
    y_max = actions_a_grouped.values.max() if not actions_a_grouped.empty else 1
    plt.yticks(np.arange(0, y_max + 1, 1))
    
    plt.grid()
    plt.tight_layout()  # Adjust layout to fit date labels
    plt.savefig("data_visual/line_chart_a.png")

def save_line_chart_b(actions_df):
    # Group by Date and count occurrences of Action "B"
    actions_b = actions_df[actions_df['Action'] == 'B']
    actions_b_grouped = actions_b.groupby("Date").size()

    plt.figure(figsize=(8, 4))
    plt.plot(actions_b_grouped.index, actions_b_grouped.values, marker="o", color="blue")
    plt.title("Line Chart for Action B")
    plt.xlabel("Date")
    plt.ylabel("Count of Action B")
    plt.xticks(rotation=45)
    
    y_max = actions_b_grouped.values.max() if not actions_b_grouped.empty else 1
    plt.yticks(np.arange(0, y_max + 1, 1))
    
    plt.grid()
    plt.tight_layout()  # Adjust layout to fit date labels
    plt.savefig("data_visual/line_chart_b.png")


def main():
	actions_df = pd.read_csv("database.csv")
	actions_df["ID"] = actions_df["ID"].fillna("").astype(int)
	actions_df['Date'] = pd.to_datetime(actions_df['Date'])
	actions_a = actions_df[actions_df['Action'] == 'A']
	actions_b = actions_df[actions_df['Action'] == 'B']
	save_table(actions_df)
	save_line_chart_a(actions_df)
	save_line_chart_b(actions_df)
