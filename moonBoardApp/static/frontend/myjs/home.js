// functions

//=============================
$(document).ready(function() {
console.log("doc "+ window.location.pathname+" ready")

function update_images(){
    d = new Date();
    $('#board-modal-img').attr("src","/static/img/current_problem.png?"+d.getTime());
    }

function set_selected(id,name,holds_setup,SH,IH,FH){
    if(id==null){
        document.getElementById("info-button").classList.add("disabled");
        document.getElementById("info-button").style.visibility = 'hidden';
    }else{
        document.getElementById("info-button").classList.remove("disabled");
        document.getElementById("info-button").style.visibility = 'visible';
    };
    $('#hold-setup').html(holds_setup.join(' + '));
    $('#SH').html(SH.join(', ') );
    $('#IH').html(IH.join(', ') );
    $('#FH').html(FH.join(', ') );
    $('#problem-name').html("<b>"+name+"</b>");
    $.post( "/_select_problem", {problem_id: id}, update_images());
};

//
if(window.location.pathname=='/problems_table'){
    //
    var problems = $('#problemstable').DataTable( {
        sDom: "t<'row'<'col-sm-2 text-left' i>><'row'<'col-sm-12 text-center'p>>",
        ajax:"_get_problems?favorites=False",
        columns: [
        { data: "name" },
        { data: "grade" },
        { data: "author" },
        { render: function ( data, type, row ) {
                    return '<input type="checkbox"  value='+ row.id + ' class="favorites">';
                }
        }],
        rowCallback: function ( row, data ) {
            // Set the checked state of the checkbox in the table
            $('input.favorites', row).prop( 'checked', data.favorite );
        },
        select:{"style":"single",
                "selector": 'td:not(:last-child)' // no row selection on last column
                },
        pagingType: "simple_numbers",
        iDisplayLength: 4
    });

//    $('#problemstable').DataTable().column(1).search('^('+$("#select-grades").val().join('$)|(^')+'$)',regex=true).draw();

    problems.on('change', 'input.favorites', function () {
       if($(this).is(":checked")) {
          console.log('add to favorites '+$(this).prop('value'));
          $.post( "/_set_as_favorites", {problem_id:$(this).prop('value'), action:"add" });
       }else{
          console.log('rm from favorites '+$(this).prop('value'));
          $.post( "/_set_as_favorites", {problem_id:$(this).prop('value'), action:"rm" });
       };
       });

    $("#select-grades").on('hide.bs.select',
    function( event ){
        var grades = $(this).val();
        if(grades == null){grades=[];}
        console.log("grades",grades);
        $('#problemstable').DataTable().column(1).search('^('+grades.join('$)|(^')+'$)',regex=true).draw();
    });

    $("#search").on('keyup',//,
    function( event ){
        console.log("text",$(this).val());
        $('#problemstable').DataTable().search($(this).val()).draw();
    });
//##################################
//
}else if(window.location.pathname=='/favorites_table'){
    var problems = $('#favoritestable').DataTable( {
        sDom: "t<'row'<'col-sm-2 text-left' i>><'row'<'col-sm-12 text-center'p>>",
        ajax:"_get_problems?favorites=True",
        columns: [
           {//data:   "active",
        render: function ( data, type, row ) {
                    return '<input type="checkbox"  value='+ row.id + ' class="delte-checkbox">';
                }
        },
        { data: "name" },
        { data: "grade" },
        { data: "author" }
        ],
        select:{"style":"single",
                "selector": 'td:not(:first-child)' // no row selection on last column
                },
        pagingType: "simple_numbers",
        iDisplayLength: 4
    });

    $('#delete-button').on( 'click', function () {
        console.log('delete checked rows');
        var table = $('#favoritestable').DataTable();
        $('input.delte-checkbox:checked').each(function(key,value){
            var problem = table.row($(value).closest('tr'));
            console.log('remove favorite ' + problem.data().id);
            $.post( "/_set_as_favorites", {problem_id:problem.data().id, action:"rm" });
            problem.remove();
//            if (table.rows('.selected').any()){
//                if(table.row('.selected').data().id==problem.data().id){
//                    set_selected(null,"",[""],[""],[""],[""]);
//                };
//            };
        });
        table.draw();
    } );

    $('#deleteall-button').on( 'click', function () {
        console.log('rm all problems from favorites ');
        $.post( "/_set_as_favorites", {problem_id:"", action:"rmall" });
        $('#favoritestable').DataTable().clear().draw();
        set_selected(null,"",[""],[""],[""],[""]);
    } );

//    $('#load-button').on( 'click', function () {
//        console.log('load favorites ');
//        $.post( "/favorites_table", {file:"contest" });
////        r.load();
//    } );

    $('#export-button').on( 'click', function () {
        console.log('export favorites ');
        $.post( "/_export_favorites", {path:"path" });
    } );

}
//else if(window.location.pathname=='/search_by_holds'){
//    var problems = $('#problemsbyholdstable').DataTable({
//        sDom: "t<'row'<'col-sm-2 text-left' i>><'row'<'col-sm-12 text-center'p>>",
//        ajax:{
//            "url": "_get_problems_by_holds",
//            "type": 'POST',
//            "data": function (d){d.holds = $('#search-txt').val();}
//            },
//        columns: [
//        { data: "name" },
//        { data: "grade" },
//        { data: "author" },
//        { render: function ( data, type, row ) {
//                    return '<input type="checkbox"  value='+ row.id + ' class="favorites">';
//                }
//        }],
//        rowCallback: function ( row, data ) {
//            // Set the checked state of the checkbox in the table
//            $('input.favorites', row).prop( 'checked', data.favorite );
//        },
//        select:{"style":"single",
//                "selector": 'td:not(:last-child)' // no row selection on last column
//                },
//        pagingType: "simple_numbers",
//        iDisplayLength: 5
//        });
//
//    $('#search-button').on('click',function(){
//        console.log($('#search-txt').val());
//        $('#problemsbyholdstable').DataTable().ajax.reload();
//    });
//
//    problems.on('change', 'input.favorites', function () {
//       if($(this).is(":checked")) {
//          console.log('add to favorites '+$(this).prop('value'));
//          $.post( "/_set_as_favorites", {problem_id:$(this).prop('value'), action:"add" });
//       }else{
//          console.log('rm from favorites '+$(this).prop('value'));
//          $.post( "/_set_as_favorites", {problem_id:$(this).prop('value'), action:"rm" });
//       };
//       });
//
//};
//######################

problems.on('select.dt', function ( e, dt, type, indexes ) {
    var problem = dt.row(indexes).data();
    console.log("Selected problem:"+ problem.id)
    set_selected(problem.id,problem.name,problem.holds_setup_short,problem.holds.SH,problem.holds.IH,problem.holds.FH);
 });

problems.on('deselect.dt', function ( e, dt, type, indexes ) {
    console.log("Deselected problem.")
    set_selected(null,"",[""],[""],[""],[""]);
 });
//
update_images();
//end document ready
});


