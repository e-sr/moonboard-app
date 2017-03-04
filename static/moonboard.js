$(document).ready(function() {
console.log('doc ready')
//
var problems = $('#problemstable').dataTable( {
        sDom: "<'row-fluid'<'span6'f>><'row-fluid'<'span6 toolbar'><'span6'>r>t<'row-fluid'<'span6'p>>",
        ajax: "_get_problems",//Flask.url_for("_get_problems"),//
        "columns": [
        { "data": "name" },
        { "data": "grade" },
        { "data": "author" }],
        select:{"style":"single"}
    });

//nzine che fa una http richiesta contenete l'id del problema selezioneto.
// todo: ritorna le informazioni per il problema selezionato e riempe lo spazio dedicato al problema selezionato

problems.on('select.dt', function ( e, dt, type, indexes ) {
    var problem = dt.row(indexes).data();
    $.post("/_select_problem", {problem_id: problem.id } );
    console.log(problem.holds.IH)
    $('#SH').html("<p>" + problem.holds.SH.join(', ') + "</p>");
    $('#IH').html("<p>" + problem.holds.IH.join(', ') + "</p>");
    $('#FH').html("<p>" + problem.holds.FH.join(', ') + "</p>");
    //$('FH') = problem.holds.FH;
    //$('SH') = problem.holds.SH;

 });

    $('#toggle-led').change(function() {
        $.post("/_toggle_led_event", {
        toggle_led: $(this).prop('checked') } );
    });



});