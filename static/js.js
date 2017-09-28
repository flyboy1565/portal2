/* Define empty values needed */
var map = null;
var infowindow = null;
var markers = [];
var new_stores_markers = [];
var dc_markers = [];
var cdk_markers = [];
/* End Empty Values */

/* Define MAPS */
var us_map_options = {
    center: {lat: 37.850033, lng: -95.6500523},
    scrollwheel: true,
    zoom: 5
};
var non_us_map_options = {
    center: {lat: 50.1166756, lng: -112.7265166},
    scrollwheel: true,
    zoom: 4
};
/* END Maps */

var ISSUE_TYPES = {
    'comm' : {'icon':'glyphicon glyphicon-signal', 'name':'Comms Downs'},
    'as400': {'icon':'glyphicon fa fa-server', 'name': 'AS400 Down'},
    'linux': {'icon': 'glyphicon fa fa-linux', 'name': 'Linux Down'},
    'unknown': {'icon': 'glyphicon fa fa-question', 'name': 'Unknown'},
    'sna': {'icon': 'glyphicon fa fa-exchange', 'name':'SNA Issues'},
}
var ISSUE_NAMES = {'P':'power', 'C': 'comm', 'S': 'sna',
    'B': 'backups', 'A': 'as400', 'L': 'linux', 'U': 'unknown',
}
var COMM_STATUS = {
    'glyphicon-arrow-down': 'label-danger',
    'glyphicon-arrow-up': 'label-success'
}
var TIMEZONES = {
        'AKST': 'America/Anchorage', 'CST': 'America/Chicago', 'EST': 'America/New_York',
        'MST': 'America/Denver', 'PST': 'America/Los_Angeles', 'HAST': 'Pacific/Honolulu'
    };

var test_email_counts_update = {
    "accel": 1,
    'att': 5,
    'cybera': 10,
    'mettel': 3,
    'windstream': 4,
    'vonage': 32,
    'cog': 3,
    'comm': 12,
    'online': 0,
    'mplus': 3,
    'xmit': 0
}
/* End TEST */

// Map Functions
function initMap() {
    if (map === null){
        map = new google.maps.Map(document.getElementById('map_container'), us_map_options);
        infowindow = new google.maps.InfoWindow();
    }
}
function load_issues(){
    $.ajax({  
        url: 'api/issues/list/?format=json',  
        success: function(data) {  
            for (var i=0; i < data.length; i++){
                var issue = create_issue(data[i]);
                add_marker(issue);
            }
        }  
    });
}
function receive_updates(){
    console.log('Socket URL: ' + 'wss://hsweb-1-flyboy1565.c9users.io/users/');
    var socket = new WebSocket('wss://hsweb-1-flyboy1565.c9users.io/users/');
    socket.onopen = function open(){
        console.log('Opened WebSocket');
    }
    socket.onmessage = event => {
        var data = JSON.parse(event.data);
        if (!data['username']){
            issue = create_issue(data);
            if (data['resolved']){
                remove_marker(issue);
            }
            else{
                add_marker(issue);
            }
        }
    }
    if (socket.readyState == WebSocket.OPEN) {
      socket.onopen();
    }
}
function add_marker(issue){
    console.log('Adding Marker: {}'.format(issue.slug));
    var myLatlng = new google.maps.LatLng(issue.latitude,issue.longitude);
    var marker = new google.maps.Marker({
        position: myLatlng,
        map: map,
        title: 'store:' + issue.store,
        store: issue.store,
        slug: issue.slug,
        issue_id: issue.issue_id,
        issue_type: issue.issue_type,
        label: issue.icon_label,
        icon: issue.icon_marker
    });
    console.log(marker.icon)
    // Infowindow setup
    var existing_marker = marker_exists(marker);
    if (!existing_marker){
        google.maps.event.addListener(marker, 'click', function () {
            $.ajax({  
                url: 'issues/{}/'.format(marker.issue_id),  
                success: function(data) {  
                    infowindow.setContent(data);
                    infowindow.open(map, marker);
                    $('#workon').click(function(e){
                        var url = $(this).data('url');
                        $.ajax({
                            url: url,
                            success: function(data){
                                issue = create_issue(data);
                                add_marker(issue);
                            }
                        });
                    });
                    $('#edit-issue-button').click(function(e){
                        var url = $(this).data('url');
                        $.ajax({
                            url: url,
                            method: 'POST',
                            success: function(data){
                                console.log('putting data into modal')
                                $('#edit-issue-modal').html(data);
                                $('#edit-issue-modal').modal('show');
                                $('#edit-issue-submit').click(function(){
                                    var pk = $('#id_pk').val();
                                    var issue_id = $('#id_issue').val(); 
                                    $.ajax({
                                        url: 'issues/edit/',
                                        method: 'POST',
                                        data: {'pk':pk, 'issue_id':issue_id},
                                        success: function(data){
                                            $('#edit-issue-modal').modal('hide');
                                        }
                                    });
                                })
                            }
                        });
                    });
                }  
            });
        });
        marker.setMap(map);
        markers.push(marker);
    }
    else{
        existing_marker.setMap(null);
        remove_marker(issue);
        add_marker(issue);
    }
    update_map_counts()
}
function remove_marker(issue){
    console.log("Remove Marker: {}".format(issue.slug));
    for (var i=0; i < markers.length; i++){
        var marker = markers[i];
        if (marker.issue_id == issue.issue_id){
            marker.setMap(null);
            markers = markers.filter(function(obj){
                return obj.issue_id !== issue.issue_id;
            });
        }
    }
}
function pop_info_window(index){
    google.maps.event.trigger(markers[index], 'click');
}
function update_map_counts(){
    issues = {'power': 0, 'comm': 0, 'sna': 0, 'backups': 0, 'as400': 0, 'linux': 0, 'uncategorized': 0}
    for (var i=0; i < markers.length; i++){
        issues[markers[i].issue_type] += 1
    }
    $('a[data-map-type="linux"] .badge').text(issues['linux']);
    $('a[data-map-type="power"] .badge').text(issues['power']);
    $('a[data-map-type="as400"] .badge').text(issues['as400']);
    $('a[data-map-type="comm"] .badge').text(issues['comm']);
    $('a[data-map-type="sna"] .badge').text(issues['sna']);
    $('a[data-map-type="uncategorized"] .badge').text(issues['uncategorized']);
    $('a[data-map-type="all"] .badge').text(markers.length);
}
function create_issue(obj){
    console.log(obj)
    if (!obj['created']  && !obj['feature']){
        var issue = {
            created: false,
            confirmed: obj['confirmed'],
            down_since: Date.parse(obj['down_since']),
            icon_marker: 'static/mapLetters/{}/letter_{}.png'.format(obj['icon'][0], obj['icon'][1].toLowerCase()),
            issue_id: obj['id'],
            issue_type: ISSUE_NAMES[obj['issue']],
            ticket: obj['ticket]'],
            vendor: obj['circuits']['vendor_name'],
            resolved: obj['resolved'],
            latitude: obj['store']['latitude'],
            longitude: obj['store']['longitude'],
            state: obj['store']['state'],
            store: obj['store']['store_number'],
            work_on: obj['workon'],
            make_slug: function(){ this.slug= (this.store + '-' + this.issue_id + '-' + this.issue_type + '-' + this.created + '-' + this.confirmed)}
        }
    }
    else{
        var issue = {
            created: obj['created'],
            confirmed: obj['feature']['confirmed'],
            down_since: Date.parse(obj['feature']['down_since']),
            icon_marker: 'static/mapLetters/{}/letter_{}.png'.format(obj['feature']['icon'][0],obj['feature']['icon'][1].toLowerCase()),
            issue_id: obj['feature']['id'],
            issue_type: ISSUE_NAMES[obj['feature']['issue']],
            vendor: obj['feature']['circuits']['vendor_name'],
            ticket: obj['feature']['ticket]'],
            resolved: obj['feature']['resolved'],
            latitude: obj['feature']['store']['latitude'],
            longitude: obj['feature']['store']['longitude'],
            state: obj['feature']['store']['state'],
            store: obj['feature']['store']['store_number'],
            work_on: obj['feature']['workon'],
            make_slug: function(){ this.slug= (this.store + '-' + this.issue_id + '-' + this.issue_type + '-' + this.created + '-' + this.confirmed)}
        }
    }
    issue.make_slug()
    return issue
}
function marker_exists(marker){
    var exists = false;
    for (var i=0; i < markers.length; i++){
        if (markers[i].issue_id == marker.issue_id){
            exists = markers[i];
        }
    }
    return exists
}
// End Map Functions
function other_markers(marker_type){
    if (marker_type == 'cdk'){
        $.ajax({  
            url: 'api/kits/?format=json',  
            success: function(data) {  
                for (var i=0; i < data.length; i++){
                    obj = data[i];
                    i = obj['store'][0];
                    var myLatlng = new google.maps.LatLng(i.latitude,i.longitude);
                    icon = 'green_wifi.png'
                    if (obj['online']){
                        icon = 'blue_wifi.png'
                    }
                    var marker = new google.maps.Marker({
                        position: myLatlng,
                        map: map,
                        title: 'store:' + i.store_number,
                        store: i.store_number,
                        icon: "static/{}".format(icon)
                    });
                    markers.push(i)
                    i.setMap(map);
                }
            }  
        });
    }
    else if (marker_type == 'dc/routers'){
        $.ajax({  
            url: 'api/devices/?format=json',  
            success: function(data) {  
                for (var i=0; i < data.length; i++){
                    obj = data[i];
                    lat = obj['location'].latitude
                    long = obj['location'].longitude
                    status = obj['status']
                    color = 'red'
                    if (status == 'UP'){
                        color = 'green'
                    }
                    if (obj['location_type'] == 'DC'){
                        letter = 'd'
                    }
                    else{
                        letter = 'r'
                    }
                    icon = 'static/mapLetters/{}/letter_{}.png'.format(color, letter)
                    var myLatlng = new google.maps.LatLng(lat, long);
                    var marker = new google.maps.Marker({
                        position: myLatlng,
                        map: map,
                        icon: icon,
                    });
                    marker.setMap(map);   
                    markers.push(marker);
                }
            }  
        });
    }
    else if (marker_type == 'new'){
        $.ajax({  
            url: 'api/locations/new_stores/?format=json',  
            success: function(data) {  
                for (var i=0; i < data.length; i++){
                    obj = data[i];
                    lat = obj.latitude
                    long = obj.longitude
                    icon = 'static/mapNumbers/green/number_{}.png'.format(obj.weeks_to_open)
                    var myLatlng = new google.maps.LatLng(lat, long);
                    var marker = new google.maps.Marker({
                        position: myLatlng,
                        map: map,
                        icon: icon,
                    });
                    marker.setMap(map);   
                    markers.push(marker);
                }
            }  
        });
    }
}
function get_timezone_time(timezone){
    var d = new Date();
    var s = d.toLocaleTimeString(undefined, { timeZone: timezone });
    $('.current_time').text(s);
};
function timeSince(date_string) {
    var startDate = new Date(date_string);
    var endDate = new Date();
    var timeDiff = Math.abs(startDate - endDate);
    var hh = Math.floor(timeDiff / 1000 / 60 / 60);
    if(hh < 10) { hh = '0' + hh; }
    timeDiff -= hh * 1000 * 60 * 60;
    var mm = Math.floor(timeDiff / 1000 / 60);
    if(mm < 10) { mm = '0' + mm; }
    timeDiff -= mm * 1000 * 60;
    var ss = Math.floor(timeDiff / 1000);
    if(ss < 10) { ss = '0' + ss; }
    return "{} hours {} minutes {} seconds".format(hh, mm ,ss)
}

function update_email_counts(providers){
    for (var provider in providers){
        var target = "li[data-provider={}] .badge".format(provider)
        $(target).text(providers[provider])
    }
}
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function get_all_kits(){
        var cdk_url = '/cdks/';
        $.ajax({  
            url: cdk_url,  
            success: function(data) {  
                $('#data-info .modal-body').html(data);
                $('#data-info .modal-title').html(header);
                $('#data-info table th').each(function(index){
                    var w = $(this).width();
                    $('#data-info table td').each(function(){
                        $(this).width(w);
                        $(this).height('30px');
                    })
                });
            }  
        });
    }
String.prototype.format = function () {
  var i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] != 'undefined' ? args[i++] : '';
  });
};

$(document).ready(function(){
    $('.dropdown-toggle').dropdown();
    $('[data-toggle="tooltip"]').tooltip(); 
    initMap();
    $('#store-search').keydown(function(e){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == 13){
            e.preventDefault();
            console.log("Enter key was hit in the store search. Did the modal pop?");
            $('#store-info-modal').modal('show');
        }
    });
    $('#map button.list-btns').click(function(){
        var target = $(this).data('target');
        var arrow_class = "glyphicon-triangle-left glyphicon-triangle-right";
        if ($('.open').attr('id') != target.replace('#', '')){
            $('.open').toggleClass('open');
            $('.glyphicon-triangle-left').toggleClass(arrow_class)
        }
        $(target).toggleClass("open");
        $(this).find('i').toggleClass(arrow_class);
    });
    $('.store-issues-filter button').click(function(){
        $(this).toggleClass('btn-primary', 'btn-default')
        var targets = 'tbody {}'.format($(this).data('target'))
        console.log(targets)
        $(targets).each(function(){
            $(targets).closest('tr').toggleClass('hidden')
        })
    })
    $('.comm-monitor-filter button').click(function(){
        $(this).toggleClass('btn-primary', 'btn-default')
        var targets = 'tbody {}'.format($(this).data('target'))
        console.log(targets)
        $(targets).each(function(){
            $(targets).closest('tr').toggleClass('hidden')
        })
    })
    $('.shsg-activity .btn').click(function(){
        $(this).toggleClass("btn-primary")
        var target = $(this).data('target')
        console.log(target)
        console.log($(target))
        $(target).each(function(){
            console.log($(this).attr('class'))
        })
        console.log("Hiddening")
        $(target).toggleClass("hidden")
        $(target).each(function(){
            console.log($(this).attr('class'))
        })
    })
    $('.report').click(function(){
        var url = $(this).data('url');
        $.ajax({
            url: url,
            success: function(data){
                $('#report-content').html(data)
            }
        })
    })
    $(window).resize(function(){
        if ($(window).width() < 1050){
            $(".full-mode").addClass('hidden');
        }
        else{
            $(".full-mode").removeClass("hidden");
        }
        // $('#data-info table th:first').each(function(){
        //     var w = $(this).width();
        //     $('#data-info table td').each(function(){
        //         $(this).width(w);
        //         $(this).height('30px');
        //     })
        // });
    });
    $("#store-info-modal").on('show.bs.modal', function(e){
        var store = $(e.relatedTarget).data("store");
        if (typeof store === 'undefined'){
            store = $('#store-search').val();
        }
        $.ajax({  
            url: 'issues/search/' + store,  
            success: function(data) {  
                console.log('Data Returned');
                $("#store-info-modal").html(data);
                time = setInterval(function(){
                    // current time
                    var timezone = $('.current_time_zone').text()
                    if (timezone != 'undefined' && timezone.length > 0){
                        console.log('updating current time')
                        get_timezone_time(TIMEZONES[timezone.split(':')[1].trim()])
                    }
                    // down since
                    $('#down-since').html(timeSince($('#down-since').data('down-since')));
                },1000);
                $('[data-toggle="tooltip"]').tooltip(); 
            }  
        });
    });
    $('a[href$="map"]').click(function(){
        $('#comm-monitor').removeClass("active");
        $('#request').removeClass("active");
        $('#reports').removeClass("active");
        $('#additional_issues').removeClass("active");
        $('.nav.navbar-nav li.active').removeClass("active");
        $('#map').addClass("in active");
    });
    $('a[href="#map"]').click(function(){
    	var issue_type = $(this).data('map-type');
    	if (issue_type != 'all'){
    	    if ($(this).hasClass('other-maps')){
    	        console.log('Getting Other Maps Icons');
                other_markers(issue_type);
            }
            for (var i=0; i < markers.length; i++){
                if (markers[i].issue_type != issue_type){
                    markers[i].setMap(null);
                }
    			else{
    				markers[i].setMap(map);
            	}
            }
        }
    	else{
    		for (var i=0; i < markers.length; i++){
                markers[i].setMap(map);
            }
        }
    });
    $('a[href="#additional_issues"]').click(function(){
        var target = $(this).attr('href')
        console.log(target)
        $.ajax({
            url: $(this).data('url'),
            success: function(data){
                $(target).find('#additional_issues_container').html(data);
            }
        })
    })
    $('#data-info').on('shown.bs.modal', function(e) {
        $('data-info .modal-body').empty()
        $('data-info .modal-title').empty()
        var data_type = $(e.relatedTarget).data('type');
        if (data_type == 'cdk'){
            header = 'CDKs'
        }
        else if (data_type == 'dc/routers'){
            header = 'DC/Routers'
        }
        else if (data_type == 'new'){
            header = 'New Stores'
        }
        var url = $(e.relatedTarget).data('url');
        console.log(url)
        $.ajax({  
            url: url,  
            success: function(data) {  
                $('#data-info .modal-body').html(data);
                $('#data-info .modal-title').html(header);
                $('#data-info button[data-toggle="tooltip"]').tooltip();
                $('#create_kit_btn').remove()
            }  
        });
    });
    $('#data-info').on('hidden.bs.modal', function(e){ 
        $('#data-info .modal-body').empty();
        $('#data-info .modal-title').empty();
        loading = '<div class="col-sm-2 col-sm-offset-5"><button class="btn btn-warning"><span class="glyphicon glyphicon-refresh glyphicon-refresh-animate"></span> Loading</button></div>';
        $('#data-info .modal-body').html(loading)
    });
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    load_issues();
    receive_updates();
});