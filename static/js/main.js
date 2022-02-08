document.addEventListener("DOMContentLoaded", function (event) {
  /*===== LINK ACTIVE =====*/
  const linkColor = document.querySelectorAll(".nav_link");

  //Show All Recent Offers

  document.querySelector(".show-all-offers").addEventListener("click", () => {
    $(".offers-div").removeClass("hidden");
    $(".home-main-wrapper").addClass("hidden");
  });

  //Show All Recent Meals

  document
    .querySelector(".show-all-top-products")
    .addEventListener("click", () => {
      $(".latest-products-div").removeClass("hidden");
      $(".home-main-wrapper").addClass("hidden");
    });

  //Show All Recent Orders

  document
    .querySelector(".show-all-recent-orders")
    .addEventListener("click", () => {
      $(".recent-orders-div").removeClass("hidden");
      $(".home-main-wrapper").addClass("hidden");
    });

  //Add Offer Button
  document.querySelector(".add-offer-btn").addEventListener("click", () => {
    $(".offers-card").addClass("hidden");
    $(".add-offer-div").removeClass("hidden");
  });
  //Way Back
  document
    .querySelector(".to-offers-from-add-offer")
    .addEventListener("click", () => {
      $(".latest-products-card").removeClass("hidden");
      $(".add-offer-div").addClass("hidden");
    });

  document.addEventListener("click", (e) => {
    if ($(e.target).hasClass("add-ingre")) {
      $(".ingredients-div").append(`
        <div class="w-100 d-flex align-items-center mt-2">
            <input type="text" class="form-control product_ingredient mx-2"> <span class="add-ingre btn text-white pb-2" style="background-color: #01CB63;">+</span>
        </div>
        `);
    }
  });

  //Add Product Button
  document.querySelector(".add-product-btn").addEventListener("click", () => {
    $(".latest-products-card").addClass("hidden");
    $(".add-product-div").removeClass("hidden");
  });
  //Way Back
  document
    .querySelector(".to-products-from-add-product")
    .addEventListener("click", () => {
      $(".latest-products-card").removeClass("hidden");
      $(".add-product-div").addClass("hidden");
    });

  //control product showing proccess

  let show_product_details = document.querySelectorAll(".show-product-details");
  show_product_details.forEach((buttonA) => {
    buttonA.addEventListener("click", (e) => {
      let p_detials = document.querySelectorAll(".p-details");
      p_detials.forEach((pd) => {
        $(pd).addClass("hidden");
      });
      let id = $(e.target).data("id");
      $(`.category-${id}-products`).addClass("hidden");
      $(`.product-${id}-details`).removeClass("hidden");
    });
  });

  //Create Offer
  document
    .querySelector(".submit-create-offer")
    .addEventListener("click", () => {
      let csrf_token_form = $(".addOffer");
      let csrf_token_input = $(csrf_token_form).children()[0];
      let csrf_token = $(csrf_token_input).val();
      let offer_name = $(".offer_name").val();
      let offer_name_ar = $(".offer_name_ar").val();
      let normal_customer_offer_description = $(
        ".normal_customer_offer_description"
      ).val();
      let agent_customer_offer_description = $(
        ".agent_customer_offer_description"
      ).val();
      let company_customer_offer_description = $(
        ".company_customer_offer_description"
      ).val();
      let supermarket_customer_offer_description = $(
        ".supermarket_customer_offer_description"
      ).val();
      let restuarant_customer_offer_description = $(
        ".restuarant_customer_offer_description"
      ).val();
      let normal_customer_offer_description_ar = $(
        ".normal_customer_offer_description_ar"
      ).val();
      let agent_customer_offer_description_ar = $(
        ".agent_customer_offer_description_ar"
      ).val();
      let company_customer_offer_description_ar = $(
        ".company_customer_offer_description_ar"
      ).val();
      let supermarket_customer_offer_description_ar = $(
        ".supermarket_customer_offer_description_ar"
      ).val();
      let restuarant_customer_offer_description_ar = $(
        ".restuarant_customer_offer_description_ar"
      ).val();
      let offer_normal_customer_price = parseInt(
        $(".offer_normal_customer_price").val()
      );
      let offer_agent_customer_price = parseInt(
        $(".offer_agent_customer_price").val()
      );
      let offer_company_customer_price = parseInt(
        $(".offer_company_customer_price").val()
      );
      let offer_supermarket_customer_price = parseInt(
        $(".offer_supermarket_customer_price").val()
      );
      let offer_restuarant_customer_price = parseInt(
        $(".offer_restuarant_customer_price").val()
      );
      let meal_id = $(".offer_meal option:selected").val();
      let meal_name = $(".offer_meal option:selected").text();
      let offer_image = document.querySelector(".offer_image").files[0];
      let offer_form = new FormData();
      offer_form.append("offer_name", `${offer_name}`);
      offer_form.append("offer_name_ar", `${offer_name_ar}`);
      offer_form.append(
        "normal_customer_offer_description",
        `${normal_customer_offer_description}`
      );
      offer_form.append(
        "agent_customer_offer_description",
        `${agent_customer_offer_description}`
      );
      offer_form.append(
        "company_customer_offer_description",
        `${company_customer_offer_description}`
      );
      offer_form.append(
        "supermarket_customer_offer_description",
        `${supermarket_customer_offer_description}`
      );
      offer_form.append(
        "restuarant_customer_offer_description",
        `${restuarant_customer_offer_description}`
      );
      offer_form.append(
        "normal_customer_offer_description_ar",
        `${normal_customer_offer_description_ar}`
      );
      offer_form.append(
        "agent_customer_offer_description_ar",
        `${agent_customer_offer_description_ar}`
      );
      offer_form.append(
        "company_customer_offer_description_ar",
        `${company_customer_offer_description_ar}`
      );
      offer_form.append(
        "supermarket_customer_offer_description_ar",
        `${supermarket_customer_offer_description_ar}`
      );
      offer_form.append(
        "restuarant_customer_offer_description_ar",
        `${restuarant_customer_offer_description_ar}`
      );
      offer_form.append(
        "normal_customer_offer_price",
        offer_normal_customer_price
      );
      offer_form.append(
        "agent_customer_offer_price",
        offer_agent_customer_price
      );
      offer_form.append(
        "company_customer_offer_price",
        offer_company_customer_price
      );
      offer_form.append(
        "supermarket_customer_offer_price",
        offer_supermarket_customer_price
      );
      offer_form.append(
        "restuarant_customer_offer_price",
        offer_restuarant_customer_price
      );
      offer_form.append("meal_id", meal_id);
      offer_form.append("offer_image", offer_image);
      console.log(offer_form);
      fetch("/offer_management/", {
        method: "POST",
        headers: {
          Authorization: `${localStorage.getItem("adminToken")}`,
          "X-CSRFToken": `${csrf_token}`,
        },
        body: offer_form,
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.message == "Offer Created Successfully") {
            $(".offers").append(`
                <div class="o-${res.offer_id} d-flex">
     
                <div class="col-4 me-1 h100 justify-content-center align-items-center">
                  <img class="w-100 mx-3" src="/${res.offer_image}">
                </div>
                <div class="col-8 h-100 text-center">
                     <h4>${meal_name}</h4>
                     <span>${offer_name}</span>
                 </div>
              </div>            
                
                `);
            $(".offers-table-body").append(`
                <tr class="offer-tr-${res.offer_id}">
                <th style="width: 30px;"><img width="80" src="/${res.offer_image}"></th>
                <td>${offer_name}</td>
                <td>${normal_customer_offer_description}</td>
                <td>
                          <div class="col-12 d-flex justify-content-between">
                            <div class="col-2 text-center">
                              <h6>Normal Customer</h6>
                              <p>${offer_normal_customer_price}$</p>
                            </div>
                            <div class="col-3 text-center">
                              <h6>Super Market Customer</h6>
                              <p>${offer_supermarket_customer_price}}$</p>
                            </div>
                            <div class="col-2 text-center">
                              <h6>Agent Customer</h6>
                              <p>${offer_agent_customer_price}$</p>
                            </div>
                            <div class="col-2 text-center">
                              <h6>Company Customer</h6>
                              <p>${offer_company_customer_price}$</p>
                            </div>
                            <div class="col-2 text-center">
                              <h6>Restaurant Customer</h6>
                              <p>${offer_restuarant_customer_price}$</p>
                            </div>
                          </div>
                </td>
              </tr>
                `);
            $(".offer_name").val("");
            $(".offer_name_ar").val("");
            $(".normal_customer_offer_description").val("");
            $(".agent_customer_offer_description").val("");
            $(".company_customer_offer_description").val("");
            $(".supermarket_customer_offer_description").val("");
            $(".restuarant_customer_offer_description").val("");
            $(".normal_customer_offer_description_ar").val("");
            $(".agent_customer_offer_description_ar").val("");
            $(".company_customer_offer_description_ar").val("");
            $(".supermarket_customer_offer_description_ar").val("");
            $(".restuarant_customer_offer_description_ar").val("");
            $(".offer_normal_customer_price").val("");
            $(".offer_agent_customer_price").val("");
            $(".offer_company_customer_price").val("");
            $(".offer_supermarket_customer_price").val("");
            $(".offer_restuarant_customer_price").val("");
            $('.offer_meal > option[selected="selected"]').removeAttr(
              "selected"
            );
            document.querySelector(".offer_image").value = "";
            alert("Offer Created Successfully");
            $(".offers-card").removeClass("hidden");
            $(".add-offer-div").addClass("hidden");
          }
        });
    });

  //Create Meal
  document
    .querySelector(".submit-create-meal")
    .addEventListener("click", () => {
      let csrf_token_form = $(".addMeal");
      let csrf_token_input = $(csrf_token_form).children()[0];
      let csrf_token = $(csrf_token_input).val();
      let meal_name = $(".meal_name").val();
      let meal_name_ar = $(".meal_name_ar").val();
      let meal_description = $(".meal_description").val();
      let meal_description_ar = $(".meal_description_ar").val();
      let customer_meal_price = parseInt($(".customer_meal_price").val());
      let supermarket_meal_price = parseInt($(".supermarket_meal_price").val());
      let company_meal_price = parseInt($(".company_meal_price").val());
      let agent_meal_price = parseInt($(".agent_meal_price").val());
      let restaurant_meal_price = parseInt($(".restuarant_meal_price").val());
      let meal_delivery_time = $(".meal_delivery_time").val();
      let category_id = $(".meal_category option:selected").val();
      let category_name = $(".meal_category option:selected").text();
      let meal_points = parseFloat($(".meal_points").val());
      let meal_main_image = document.querySelector(".meal_main_image").files[0];
      let meal_images = document.querySelector(".meal_images").files;

      let meal_form = new FormData();
      for (let index = 0; index < meal_images.length; index++) {
        meal_form.append("meal_image", meal_images[index]);
      }

      document.querySelectorAll(".product_ingredient").forEach((ingre) => {
        console.log(`${$(ingre).val()}`);
        meal_form.append("ingredients", `${$(ingre).val()}`);
      });
      meal_form.append("meal_name", `${meal_name}`);
      meal_form.append("meal_name_ar", `${meal_name_ar}`);
      meal_form.append("meal_description", `${meal_description}`);
      meal_form.append("meal_description_ar", `${meal_description_ar}`);
      meal_form.append("customer_meal_price", customer_meal_price);
      meal_form.append("supermarket_meal_price", supermarket_meal_price);
      meal_form.append("company_meal_price", company_meal_price);
      meal_form.append("agent_meal_price", agent_meal_price);
      meal_form.append("restaurant_meal_price", restaurant_meal_price);
      meal_form.append("category_id", category_id);
      meal_form.append("meal_points", meal_points);
      meal_form.append("meal_delivery_time", meal_delivery_time);
      meal_form.append("meal_main_image", meal_main_image);
      fetch("/meal_management/", {
        method: "POST",
        headers: {
          Authorization: `${localStorage.getItem("adminToken")}`,
          "X-CSRFToken": `${csrf_token}`,
        },
        body: meal_form,
      })
        .then((res) => res.json())
        .then((res) => {
          if (res.message == "Meal Created Successfully") {
            alert("Meal Created Successfully");
            $(".products").append(`
              
                  <div class="p-{{meal_object.meal.meal_id}} d-flex">
                    <div class="col-4 me-1 h100 justify-content-center align-items-center"><img class="w-100" src='/{{meal_object.meal.meal_main_image}}'></div>

                    <div class="col-8 h-100 text-center">
                        <h4>${meal_name}</h4>
                        <span class="w-100">
                        <i class='bx bx-star' style="color: #F86161;font-size:1.4rem"></i>
                        <i class='bx bx-star' style="color: #F86161;font-size:1.4rem"></i>
                        <i class='bx bx-star' style="color: #F86161;font-size:1.4rem"></i>
                        <i class='bx bx-star' style="color: #F86161;font-size:1.4rem"></i>
                        <i class='bx bx-star' style="color: #F86161;font-size:1.4rem"></i>
                    </span>
                        <p>Ordered 0 Times</p>
                    </div>
               </div>
            `);
            $(".meal_tables").append(`
            <tr class="offer-tr-${res.meal_id}">
            <th style="width: 30px;"><img width="80" src="/${res.meal_main_image}"></th>
            <td>${meal_name}</td>
            <td>${meal_description}</td>
            <td>
                      <div class="col-12 d-flex justify-content-between">
                        <div class="col-2 text-center">
                          <h6>Normal Customer</h6>
                          <p>${customer_meal_price}$</p>
                        </div>
                        <div class="col-3 text-center">
                          <h6>Super Market Customer</h6>
                          <p>${supermarket_meal_price}$</p>
                        </div>
                        <div class="col-2 text-center">
                          <h6>Agent Customer</h6>
                          <p>${agent_meal_price}$</p>
                        </div>
                        <div class="col-2 text-center">
                          <h6>Company Customer</h6>
                          <p>${company_meal_price}$</p>
                        </div>
                        <div class="col-2 text-center">
                          <h6>Restaurant Customer</h6>
                          <p>${restaurant_meal_price}$</p>
                        </div>
                      </div>
            </td>
            <td>
            0
            </td>
        <td>

        </td>
          </tr>
            `);
            $(".ingredients-div").empty();
            $(".ingredients-div").append(`
        <div class="w-100 d-flex align-items-center mt-2">
            <input type="text" class="form-control product_ingredient mx-2"> <span class="add-ingre btn text-white pb-2" style="background-color: #01CB63;">+</span>
        </div>
        `);
            $(".meal_name").val("");
            $(".meal_name_ar").val("");
            $(".meal_description").val("");
            $(".meal_description_ar").val("");
            $(".customer_meal_price").val("");
            $(".supermarket_meal_price").val("");
            $(".company_meal_price").val("");
            $(".agent_meal_price").val("");
            $(".restuarant_meal_price").val("");
            $('.meal_category > option[selected="selected"]').removeAttr(
              "selected"
            );
            document.querySelector(".meal_main_image").value = "";
            document.querySelector(".meal_images").value = "";
            $(".latest-products-card").removeClass("hidden");
            $(".add-product-div").addClass("hidden");
          }
        });
    });

  //Navigation In Breadcrumb
  document.querySelectorAll(".to-dash").forEach((toDash) => {
    toDash.addEventListener("click", () => {
      $(".offers-div").addClass("hidden");
      $(".latest-products-div").addClass("hidden");
      $(".recent-orders-div").addClass("hidden");
      $(".add-offer-div").addClass("hidden");
      $(".add-product-div").addClass("hidden");

      $(".home-main-wrapper").removeClass("hidden");
      $(".latest-products-card").removeClass("hidden");
      $(".offers-card").removeClass("hidden");
    });
  });

  /*     
    function colorLink(){
    if(linkColor){
    linkColor.forEach(l=> l.classList.remove('active'))
    this.classList.add('active')
    }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink)) */

  // Your code to run since DOM is loaded and ready
});
