import csv


def main():
    #declare vars
    prod_rev, prod_qty, daily_rev, total_rev = calculate_from_file() #get multiple values from func
    highest_day = None
    highest_revenue = 0.0

    #loop through dailty revenue to find highest daily revenue
    for day, rev in daily_rev.items():
        if rev > highest_revenue:
            highest_revenue = rev
            highest_day = day
    
    make_report(total_rev, highest_day, highest_revenue, prod_rev, prod_qty)#call func to generate txt report of data
    make_summary(prod_rev,prod_qty)#call func to generate csv summart of data



def calculate_from_file():
    """Calculates different stats based on revenue quantity and dates

    Returns:
        Tuple: product_revenue > dict. Product_quantity > dict. daily_revenue > dict. total_revenue > float.
    """    
    #initialize vars
    product_revenue = {}
    product_quantity = {}
    total_revenue = 0.0
    daily_revenue = {}
    
    with open("sales_data.csv", "r") as file:
        reader = csv.DictReader(file)
        
        #loop through data in file and record relevant data into vars
        for row in reader:
            line_revenue = int(row["quantity"]) * float(row["price"])
            product_name = row["product"]
            line_quantity = int(row["quantity"])
            line_date = row["date"]
            
            #initialize keys 
            if product_name not in product_revenue:
                product_revenue[product_name] = 0.0
                
            if line_date not in daily_revenue:
                daily_revenue[line_date] = 0.0
                
            if product_name not in product_quantity:
                product_quantity[product_name] = 0
            
            #add data to dicts and float
            product_revenue[product_name] += line_revenue
            product_quantity[product_name] += line_quantity
            daily_revenue[line_date] += line_revenue
            total_revenue += line_revenue
            
    return product_revenue, product_quantity, daily_revenue, total_revenue

def make_report(total,highest_day, highest_rev, product_rev, product_qty):
    """Generates a txt file containing various stats about relvant sales data

    Args:
        total (float): total revenue
        highest_day (string): date where the highest revenue was collected
        highest_rev (float): amount of revenue earned on the highest revenue date
        product_rev (dict): [product] > total revenue for product
        product_qty (dict): [product] > total quantity for product
    """    
    with open("sales_report.txt", "w") as file:
        file.write("===   Sales Report   ===\n\n")
        file.write(f"Overall Total Revenue: {total:.2f}\n")
        file.write(f"Highest Revenue Day: {highest_day} -> ${highest_rev}\n")
        file.write("\n---   Product Revenue   ---\n\n")
        for product, rev in product_rev.items():
            file.write(f"{product}: ${rev:.2f}\n")
        file.write("\n---   Product Quantity   ---\n\n")
        for product, quant in product_qty.items():
            file.write(f"{product}: {quant}\n")

def make_summary(product_rev, product_qty):
    """Generates a csv file containing relevant sales data

    Args:
        product_rev (dict): [product] > total revenue for product
        product_qty (dict): [product] > total quantity for product
    """    
    with open("product_summary.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["product", "total_quantity","total_revenue"])
        writer.writeheader()
    
        for product in product_rev:
            writer.writerow({"product": product,
                            "total_quantity": product_qty[product],
                            "total_revenue": product_rev[product]
                            })

if __name__ == "__main__":
    main()