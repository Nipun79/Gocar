
    // Use Javascrip
    function pick(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth()+1; 
    var yyyy = today.getFullYear();
    if(dd<10){
        dd='0'+dd
    } 
    if(mm<10){
        mm='0'+mm
    } 
    var hour=today.getHours()
    var min=today.getMinutes()

    today = yyyy+'-'+mm+'-'+dd;
    document.getElementById("startdate").setAttribute("min", today);
    document.getElementById("enddate").setAttribute("min",document.getElementById("startdate").value);
 
    var y=document.getElementById("enddate").valueAsDate
    var x=document.getElementById("startdate").valueAsDate
    diff=y-x
    diff=diff/(1000 * 60 * 60 * 24)
    if(diff==0){
    document.getElementById("NumberOfDays").value=1 
    }
    else{
    document.getElementById("NumberOfDays").value=diff
    }
 }
