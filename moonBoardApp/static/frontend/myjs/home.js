// functions
function update_images(){
    d = new Date();
    $('#board-img').attr("src","/static/img/current_problem.png?"+d.getTime());
    $('#board-modal-img').attr("src","static/img/current_problem.png?"+d.getTime());
    }

function toggle_fullscreen(e){
    console.log('toggle fullscreen');
    //
    if (!document.webkitFullscreenElement){
        document.documentElement.webkitRequestFullscreen();
    }else{
        document.webkitExitFullscreen();
    }
};

//=============================
$(document).ready(function() {
document.body.style.zoom = "80%";
console.log("doc ready")
//
update_images();
//
var socket = io.connect('http://' + document.domain + ':' + location.port );
//
var problems = $('#problemstable').dataTable( {
        sDom: "<'row'<'col-sm-8 text-left'><'col-sm-4 text-right'p>>t<'row'<'col-sm-12 text-left'i>>",
        ajax:"_get_problems",
        //ajax:Flask.url_for("_get_problems"),
        "columns": [
        { "data": "name" },
        { "data": "grade" },
        { "data": "author" }],
        select:{"style":"single"},
        pagingType: "simple",
        iDisplayLength: 10
    });

problems.on('select.dt', function ( e, dt, type, indexes ) {
    var problem = dt.row(indexes).data();
    console.log("Selected problem:"+ problem.id)
    $('#hold-setup').html(problem.holds_setup_short.join(' + ') );
    $('#SH').html( problem.holds.SH.join(', ') );
    $('#IH').html( problem.holds.IH.join(', ') );
    $('#FH').html( problem.holds.FH.join(', ') );
    $('#board-modal-title').html( problem.name );
    $('#problem-name').html( "<b>"+problem.name+"</b>");
    $.post( "/_select_problem", {problem_id: problem.id }, update_images());
 });

problems.on('deselect.dt', function ( e, dt, type, indexes ) {
    console.log("Deselected problem.")
    $('#hold-setup').html("" );
    $('#SH').html("");
    $('#IH').html("");
    $('#FH').html("");
    $('#board-modal-title').html("");
    $('#problem-name').html("");
    $.post( "/_select_problem", {problem_id: null}, update_images());
 });

$("#select-grades").on('changed.bs.select',
    function( event ){
        var grades = $(this).val();
        if(grades == null){grades=[];}
        console.log("grades",grades);
        $('#problemstable').DataTable().column(1).search('^('+grades.join('$)|(^')+'$)',regex=true).draw();
});

$("#search").on('keyup',//'hide.bs.select',
    function( event ){
        console.log("text",$(this).val());
        $('#problemstable').DataTable().search($(this).val()).draw();
});

document.getElementById("fullscreen-btn").addEventListener("click",toggle_fullscreen);

//end document ready
});


