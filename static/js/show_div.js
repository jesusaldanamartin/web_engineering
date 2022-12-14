const btn = document.querySelector("#show-user-div")
const container = document.querySelector("#user-div")

btn.addEventListener("click", function(){
    if(container.style.display === "block"){
        container.style.display = "none";
        btn.textContent = 'Mostrar Usuarios'
    } else{
        container.style.display = "block";
        btn.textContent = 'Ocultar Usuarios'
    }

});

const btn2 = document.querySelector("#show-task-div")
const container2 = document.querySelector("#task-div")

btn2.addEventListener("click", function(){
    if(container2.style.display === "block"){
        container2.style.display = "none";
        btn2.textContent = 'Mostrar Tareas'
    } else{
        container2.style.display = "block";
        btn2.textContent = 'Ocultar Tareas'
    }
});

const btn3 = document.querySelector("#show-robot-div")
const container3 = document.querySelector("#robot-div")

btn3.addEventListener("click", function(){
    if(container3.style.display === "block"){
        container3.style.display = "none";
        btn3.textContent = 'Mostrar Robots'
    } else{
        container3.style.display = "block";
        btn3.textContent = 'Ocultar Robots'
    }
});

const btn4 = document.querySelector("#show-everything")
btn4.addEventListener("click", function(){

    if(btn4.textContent == 'Ocultar Todo'){
        container.style.display = "none";
        container2.style.display = "none";
        container3.style.display = "none";
        btn4.textContent = 'Mostrar Todo'
    } else{
        container.style.display = "block";
        container2.style.display = "block";
        container3.style.display = "block";
        btn4.textContent = 'Ocultar Todo'
    }
});

// No funciona ?
// if(container.style.display == "block" &&
//         container2.style.display == "block" &&
//         container3.style.display == "block") {
//             btn4.textContent == 'Ocultar Todo'
//     }
