/* Default values for the initial load */
var INITIAL_LAT=37.7833,
    INITIAL_LONG=-122.4167,
    RADIUS=1,
    DEFAULT_CATEGORY="All",
    COLORS = ['#FFC0CB', '#FF7F50', '#FFDEAD', '#FFA500', '#FFD700',
	      '#9ACD32', '#AFEEEE', '#1E90FF', '#6495ED', '#FA8072'
	     ];

/* Backbone module for the trucks views */
(function ($) {

    // Truck Model
    var Truck = Backbone.Model.extend({
        defaults: {
            applicant: "Truck", 
            category: "Food", 
            // Default coordinates of SF
            latitude: 37.7833, 
            longitude: -122.4167
        }
    });

    // View for each Truck div
    var TruckView = Backbone.View.extend({
        tagName: "div",
        className: "truckContainer",
        template: $("#truckTemplate").html(),

        render: function () {
            var tmpl = _.template(this.template);
            this.$el.html(tmpl(this.model.toJSON()));
            return this;
        }

    });

    // Category Model
    var Category = Backbone.Model.extend({
	defaults: {
	    name: 'Food',
	    count: 1
	}
    });
    
    //  View for each Category div 
    var CategoryView = Backbone.View.extend({
	tagName: "div",
	className: "categoryContainer",
	template: $("#categoryTemplate").html(),
	render: function () {
	    var tmpl = _.template(this.template);
	    var randomColorIndex = parseInt(Math.random()* 100) % 10;
	    this.model['color'] = COLORS[randomColorIndex]
	    this.$el.html(tmpl(this.model));
	    return this;
	}
	
    });

    // Collection of Trucks
    var truckCollection = Backbone.Collection.extend({
        model: Truck,
        // The API root for the trucks:
        url: '/api/trucks',
        parse: function(data){
            return data;
        }
    });

    // View of the collection of Trucks
    var trucksView = Backbone.View.extend({

        el: $("#trucks"),


        /**
         * Initialize the truck View
         *
         * When called, it will fetch the main collection of the trucks, 
         * initialize the default initial values for this truck views, 
         * create the main map in its container and load the default markers.
         *
         */
        initialize: function () {

            this.collection = new truckCollection();
            this.fillInitializeFields();

            // Creating the map in the map_container with some main options
            var initLatlng = new google.maps.LatLng(INITIAL_LAT, INITIAL_LONG);
            var mapOptions = {
                zoom: 14,
                center: initLatlng
            }
            this.map = new google.maps.Map(document.getElementById('map_container'), mapOptions);
            this.addMapMenu();

            // Set the markers (location and trucks) of the map
            this.markers = [];
            this.renderList();
        },
        
        /**
         * Set the default values at first load in the form
         */
        fillInitializeFields: function () {
            var form = $('form#getTrucks'), 
                latitude = form.find('#latitude'), 
                longitude = form.find('#longitude'), 
                radius = form.find('#radius'),
                category = form.find('#category');

            latitude.val(INITIAL_LAT);
            longitude.val(INITIAL_LONG);
            radius.val(RADIUS);
            category.val(DEFAULT_CATEGORY);

        },

        /**
         * Set the click event options on the map.
         *
         * The right click will help the user to choose another location on the 
         * map. The normal click (left) would clear any left menu created by the
         * former right click if any.
         * 
         */
        addMapMenu: function () {

            // Saving this object in `that` variable:
            var that = this;

            google.maps.event.addListener(this.map, 
                                          "rightclick", 
                                          function(event) {
                                              showContextMenu(event.latLng, that);
                                          }, that);

            google.maps.event.addListener(this.map, 
                                          "click", 
                                          function(event) {
                                              clearSetMenu();
                                          }, that);;


        },

        /**
         * Render the list of trucks points and the location selected
         * @param {Object} event
         */
        renderList: function (e) {

            if (e !== undefined) {
                // We do not want the page to reload as the event is
                // from a form
                e.preventDefault();
            }

            var form = $('form#getTrucks'), 
                latitude = form.find('#latitude'), 
                longitude = form.find('#longitude'), 
                radius = form.find('#radius'),
                category = form.find('#category');
            var cat_val = category.val() == 'All' ? '' : category.val()
            
            // Set up the param data of the request
            var data = {
                'latitude': latitude.val(),
                'longitude': longitude.val(),
                'radius': radius.val(),
                'category': cat_val
            };

            // Set the options of the get request
            var options = {
                async: false, 
                traditional: true,
                data: data,
                processData: true
            }

            // Get the udpated list
            this.collection.fetch(options);

            // Clean the former list of markers of the map
            this.cleanTrucksList();
            
            // Center to the new position
            this.setCenterMarker(latitude.val(), longitude.val());

            // Show the list on the right as well as the markers on the map
            this.showTotal(this.collection.models.length);
            that = this;
	    var categories = {};
            _.each(this.collection.models, function (truck) {
		// Adding the category in the categories object
		if (!(truck.attributes.category in categories)) {
		    categories[truck.attributes.category] = 0;
		}
		categories[truck.attributes.category] ++;

		// Render the truck
                var divEl = that.renderTruck(truck);
                that.addTruckToMap(truck, divEl);

            }, this, categories);

	    this.showCategories(categories);

        },

        
        /**
         * Set the new location selected marker and cetner the map around
         * it.
         * @param {Object} latitude: Latitude of the center position
         * @param {Object} longitude: Longitude of the center position
         */
        setCenterMarker: function (latitude, longitude) {
            var pointLatlng = new google.maps.LatLng(latitude, longitude);

            var marker = new google.maps.Marker({
                position: pointLatlng,
                map: this.map,
                title: '',
                icon: "http://maps.google.com/mapfiles/ms/icons/green-dot.png"
            });

            var latLng = marker.getPosition();

            this.map.setCenter(latLng); 
            this.markers.push(marker);
        },

        /**
         * Clean the map of the former markers and the list on the right
         */
        cleanTrucksList: function () {
            
            clearSetMenu();
            this.$el.find('#trucks_list').find("#list").html("");

            for (var i = 0; i < this.markers.length; i++) {
                this.markers[i].setMap(null);
            }
            this.markers.splice(0, this.markers.length);

	    // Clean as well the categories div:
	    this.$el.find('#categories_list').find('#list').html("");
        },


	/**
	 * Show the different categories for the selection
	 * @param {Object} categories
	 */
	showCategories: function (categories) {
	    var total = 0, 
	        sortable = [];

	    // Let's sort them by count
	    for (var category in categories) {
		 sortable.push([category, categories[category]])
	    }
	    sortable.sort(function(a, b) {return b[1] - a[1]})

	    _.each(sortable, function (el) {
		total ++;
		count = el[1];
		category = el[0];
		var categoryElView = new CategoryView({ model: {
		    name: category,
		    count: count
		}});
		var divEl = categoryElView.render().el;

		this.$el.find('#categories_list').find('#list').append(divEl);
		
	    }, this, total);

	    var totalDiv = this.$el.find('#categories_list').find('#total');
	    totalDiv.html("<b>Number of Categories: " + total + "</b>"); 
	},

        /**
         * Show the total number of trucks from the updated list
         * @param {{Number} number of trucks
         */
        showTotal: function (number) {
            var totalDiv = this.$el.find('#trucks_list').find('#total');
            totalDiv.html("<b>Number of Trucks: " + number + "</b>");
        },


        /**
         * Call the truck view to show on the right list
         * @param {Object} truck
         * @return {Object} Div element
         */
        renderTruck: function (truck) {
            var truckElView = new TruckView({model: truck}), 
                divEl = truckElView.render().el;

            this.$el.find('#trucks_list').find("#list").append(divEl);

            return divEl;
        },


        /**
         * Add the truck to the map as new marker
         * @param {Object} Truck to add in the map
         * @param {Object} divEl its div
         */
        addTruckToMap: function (truck, divEl) {

            var lat = truck.attributes.latitude, 
                lon = truck.attributes.longitude;

            var truckLatlng = new google.maps.LatLng(lat, lon);

            var marker = new google.maps.Marker({
                position: truckLatlng,
                map: this.map,
                icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
            });

            this.markers.push(marker);

            // Adding the tooltip here:
            var infowindow = new google.maps.InfoWindow({
                content:  truck.attributes.applicant
            });

            google.maps.event.addListener(marker, 'click', function() {
                infowindow.open(this.map, marker);
            });

            // Adding the 2 main events on highlighting the marker when on mouse
            divEl.addEventListener("mouseover", function () {
                marker.setIcon("http://maps.google.com/mapfiles/ms/icons/blue-dot.png");
            }, marker);
            divEl.addEventListener("mouseleave", function () {
                marker.setIcon("http://maps.google.com/mapfiles/ms/icons/red-dot.png");
            }, marker);

        },

        /* Set up the events */
        events: {
            'click #getListTrucks': "renderList"
        }

    });

    var trucks = new trucksView();
    

} (jQuery))
