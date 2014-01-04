function submit_one() {    
    //document.getElementById('atab2').setAttribute('data-toggle','tab');
    //var form = document.getElementById('form_info');
    //alert(form.submit.name);
    $('#myTab a[href="#tab2"]').tab('show');
    
}

function submit_two() {    
    $('#myTab a[href="#tab3"]').tab('show');
}

function submit_three() {    
    $('#myTab a[href="#tab4"]').tab('show');
}

function submit_four(f) {
    f.submit();
}

function back_two() {    
    $('#myTab a[href="#tab1"]').tab('show');
}

function back_three() {    
    $('#myTab a[href="#tab2"]').tab('show');
}

function back_four() {    
    $('#myTab a[href="#tab3"]').tab('show');
}

function cancel_me() {
    alert('hi');
}
