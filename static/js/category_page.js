$(document).ready(()=>{



    //Create Category
    document.querySelector('.create-category').addEventListener('click', ()=>{
        let category_name = $('.category_name').val()
        let category_name_ar = $('.category_name_ar').val()
        let category_image =  document.querySelector('.category_image').files[0]
        let csrf_token_form = $('.addCategory')
        let csrf_token_input = $(csrf_token_form).children()[0]
        let csrf_token = $(csrf_token_input).val()

        category_form = new FormData()
        category_form.append('category_name', category_name)
        category_form.append('category_name_ar', category_name_ar)
        category_form.append('category_image', category_image)

        fetch('/category_manaegment/', {
            method : "POST", 
            headers : {
                "Authorization" : `${localStorage.getItem('adminToken')}`,
                "X-CSRFToken" : `${csrf_token}`
            },
            body : category_form
        }).then(res=>res.json()).then(res=>{
            alert('Category Created Successfully')
            $('.category_name').val('')
            $('.category_name_ar').val('')
            document.querySelector('.category_image').value = ""


            $('.categories-main-div').append(`
            <div class="card mx-1 border-primary mb-3">
      
      
            <div class="card-header d-flex justify-content-between">
              <b>${category_name}</b>
              <a class="show-category-products" id="${res.category_id}" href="#">Show All</a>
            </div>
           
           
            <div class="card-body card-scroll">
    
        
            </div>
    
    
          </div>
            
            `)
        })

    })
    

    //Edit Meal
    document.querySelectorAll('.submit-edit-meal').forEach(a => a.addEventListener('click', (e)=>{
        console.log('in')
        let csrf_token_form = $('.addCategory')
        let csrf_token_input = $(csrf_token_form).children()[0]
        let csrf_token = $(csrf_token_input).val()
        let meal_name =                       $('.meal_name').val()
        let meal_name_ar =                    $('.meal_name_ar').val()
        let meal_description =                $('.meal_description').val()
        let meal_description_ar =             $('.meal_description_ar').val()
        let customer_meal_price = parseInt(   $('.customer_meal_price').val())
        let supermarket_meal_price = parseInt($('.supermarket_meal_price').val())
        let company_meal_price = parseInt(    $('.company_meal_price').val())
        let agent_meal_price = parseInt(      $('.agent_meal_price').val())
        let restaurant_meal_price = parseInt( $('.restuarant_meal_price').val())
        let category_id = $('.meal_category option:selected').val()
        let meal_points = parseFloat($('.meal_points').val()) 
        let meal_delivery_time = $('.meal_delivery_time').val()
/*         let meal_main_image = document.querySelector('.meal_main_image').files[0]
        let meal_images = document.querySelector('.meal_images').files
         */
        let meal_form = new FormData()
/*         for (let index = 0; index < meal_images.length; index++) {
          meal_form.append('meal_image', meal_images[index])      
        } */
    
/*         document.querySelectorAll('.product_ingredient').forEach(ingre=>{
          console.log(`${$(ingre).val()}`)
          meal_form.append('ingredients', `${$(ingre).val()}`)
      }) */
      JSON.stringify({
        'meal_id': `${e.target.id}`,
        'meal_name': `${meal_name}`,
        'meal_name_ar': `${meal_name_ar}`,
        'meal_description': `${meal_description}`,
        'meal_description_ar': `${meal_description_ar}`,
        'customer_meal_price': customer_meal_price,
        'supermarket_meal_price': supermarket_meal_price,
        'company_meal_price': company_meal_price,
        'agent_meal_price': agent_meal_price,
        'meal_delivery_time': meal_delivery_time,
        'restaurant_meal_price': restaurant_meal_price,
        'category_id': category_id,
        'meal_points': meal_points,
        'meal_delivery_time': meal_delivery_time,
       // meal_form.append('meal_main_image': meal_main_image)
      })
        fetch('/meal_management/', {
            method: "PUT",
            headers : {
                "Authorization" : `${localStorage.getItem('adminToken')}`,
                "X-CSRFToken" : `${csrf_token}`
            },
            body: `meal_form`
        }).then(res=>res.json()).then(res=>{
                alert("Meal Updated Successfully")
                location.reload()

        })
    
        })  
    )


    document.addEventListener('click', (e)=>{
        if($(e.target).hasClass('show-category-products')){
            $('.categories-wrapper').addClass('hidden')
            $(`.category-${e.target.id}-products`).removeClass('hidden')
        }
        else if ($(e.target).hasClass('show-product-details')){
            $('.categories-wrapper').addClass('hidden')
            $(`.category-${$(e.target).data('categoryid')}-products`).addClass('hidden')
            $(`.product-${e.target.id}-details`).removeClass('hidden')
        }
        else if ($(e.target).hasClass('go-to-main-category-div')){
            $('.categories-wrapper').removeClass('hidden')
            $(`.category-${e.target.id}-products`).addClass('hidden')
        }
        else if ($(e.target).hasClass('go-to-main-category-div-from-product')){
            $('.categories-wrapper').removeClass('hidden')
            $(`.product-${e.target.id}-details`).addClass('hidden')

        }
        else if ($(e.target).hasClass('go-to-product-category')){
            
            $(`.product-${e.target.id}-details`).addClass('hidden')

            $(`.category-${$(e.target).data('categoryid')}-products`).removeClass('hidden')
        }
        

        else if($(e.target).hasClass('delete-product')){
            let answer = prompt('Type y To Confirm Delete')
            if( answer == "y"){
            let csrf_token_form = $('.addCategory')
            let csrf_token_input = $(csrf_token_form).children()[0]
            let csrf_token = $(csrf_token_input).val()
            fetch(`/meal_management/`, {
                method : "DELETE", 
                headers : {
                    "Authorization" : `${localStorage.getItem('adminToken')}`,
                    "X-CSRFToken" : `${csrf_token}`
                },
                body : JSON.stringify({
                    "meal_id" : `${e.target.id}`
                })
            }).then(res=>res.json()).then(res=>{
                alert('Meal Deleted Successfully')
                $(`.meal-${e.target.id}`).remove()
                $(`.m-${e.target.id}`).remove()
            })
        }
        }

        else if($(e.target).hasClass('delete-category')){
            if(prompt('Type y To Confirm Delete') == "y"){
            let csrf_token_form = $('.addCategory')
            let csrf_token_input = $(csrf_token_form).children()[0]
            let csrf_token = $(csrf_token_input).val()
            fetch(`/category_managment/`, {
                method : "DELETE", 
                headers : {
                    "Authorization" : `${localStorage.getItem('adminToken')}`,
                    "X-CSRFToken" : `${csrf_token}`
                },
                body : JSON.stringify({
                    "category_id" : `${e.target.id}`
                })
            }).then(res=>res.json()).then(res=>{
                alert('Category Deleted Successfully')
                $(`.category-${e.target.id}-products`).remove()
                $(`.category-${e.target.id}-card`).remove()
            })
        }
    }
    })


    
})