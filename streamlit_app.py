# Import python packages


import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smooothie!
    """
)

name_on_order = st.text_input('Name on Smoothie :')
st.write('The name on smoothie will be ', name_on_order)

#option = st.selectbox(
   # "How would you like to be contacted?",
    #("Email", "Home phone", "Mobile phone"),
#)

#st.write("You selected:", option)

session = get_active_session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list=st.multiselect('Choose up to 5 ingredients:'
                                ,my_dataframe
                                ,max_selections=5)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen
        
    #st.write(ingredients_string)
    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    time_to_insert=st.button('Submit Order')

    st.write(my_insert_stmt)
    #st.stop()
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
         