import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import re
import seaborn as sns

def plot_histogram(df, col):
    plt.figure()
    sns.histplot(df[col].dropna(), kde=True)
    plt.title(f'Distribution of {col}')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_scatter(df, x_col, y_col):
    plt.figure()
    sns.scatterplot(x=df[x_col], y=df[y_col])
    plt.title(f'{y_col} vs {x_col} Plot')
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_boxplot(df, col):
    plt.figure()
    sns.boxplot(x=df[col])
    plt.title(f'Boxplot of {col}')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_correlation_heatmap(df):
    plt.figure(figsize=(10, 8))
    corr = df.select_dtypes(include='number').corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
    plt.title("Correlation Heatmap")
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_bar_chart_counts(df, col):
    plt.figure()
    counts = df[col].value_counts()
    sns.barplot(x=counts.index, y=counts.values)
    plt.title(f'Counts of {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def plot_pie_chart(df, col):
    plt.figure()
    counts = df[col].value_counts()
    plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    plt.title(f'Distribution of {col}')
    plt.ylabel('')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_plot_from_prompt(df, prompt):
    print(f"DEBUG: Starting prompt parsing for: '{prompt}'")
    prompt_lower = prompt.lower()
    plot_base64 = None



    # Handle "compare X and Y" or "compare X vs Y"
    match_compare = re.search(r'compare\s+([\w\s]+?)\s+(?:and|vs)\s+([\w\s]+)', prompt_lower)
    if match_compare:
        print("DEBUG: Prompt matched 'compare' pattern.")
        try:
            col1_str = match_compare.group(1).strip()
            col2_str = match_compare.group(2).strip()
            
            df_cols_cleaned = [c.lower().replace(" ", "") for c in df.columns]
            col1_cleaned = col1_str.replace(" ", "")
            col2_cleaned = col2_str.replace(" ", "")

            print(f"DEBUG: Found cleaned columns: '{col1_cleaned}' and '{col2_cleaned}'")

            if col1_cleaned in df_cols_cleaned and col2_cleaned in df_cols_cleaned:
                original_col1 = df.columns[df_cols_cleaned.index(col1_cleaned)]
                original_col2 = df.columns[df_cols_cleaned.index(col2_cleaned)]
                
                if pd.api.types.is_numeric_dtype(df[original_col1]) and pd.api.types.is_numeric_dtype(df[original_col2]):
                    print("DEBUG: Generating scatter plot.")
                    plot_base64 = plot_scatter(df, original_col1, original_col2)
            else:
                print("DEBUG: Column names not found in dataset.")
        except IndexError:
            print("DEBUG: Regex failed to extract all groups.")
            pass
    
    # Handle "distribution of X" or "bar chart for X" or "pie chart for X"
    match_dist_bar_pie = re.search(r'(distribution of|bar chart for|pie chart for)\s+([\w\s]+)', prompt_lower)
    if match_dist_bar_pie and not plot_base64:
        plot_type = match_dist_bar_pie.group(1).strip()
        col_str = match_dist_bar_pie.group(2).strip()
        df_cols_cleaned = [c.lower().replace(" ", "") for c in df.columns]
        col_cleaned = col_str.replace(" ", "")
        
        if col_cleaned in df_cols_cleaned:
            original_col = df.columns[df_cols_cleaned.index(col_cleaned)]
            if plot_type == 'distribution of':
                plot_base64 = plot_histogram(df, original_col)
            elif plot_type == 'bar chart for':
                plot_base64 = plot_bar_chart_counts(df, original_col)
            elif plot_type == 'pie chart for':
                plot_base64 = plot_pie_chart(df, original_col)

    # Handle "correlation" or "heatmap"
    if not plot_base64 and ('correlation' in prompt_lower or 'heatmap' in prompt_lower):
        plot_base64 = plot_correlation_heatmap(df)

    # Handle "boxplot" or "outliers of X"
    match_box = re.search(r'(boxplot|outliers of)\s+([\w\s]+)', prompt_lower)
    if match_box and not plot_base64:
        col_str = match_box.group(2).strip()
        df_cols_cleaned = [c.lower().replace(" ", "") for c in df.columns]
        col_cleaned = col_str.replace(" ", "")

        if col_cleaned in df_cols_cleaned:
            original_col = df.columns[df_cols_cleaned.index(col_cleaned)]
            plot_base64 = plot_boxplot(df, original_col)
    
    return plot_base64