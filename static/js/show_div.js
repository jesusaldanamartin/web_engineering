const btn = document.querySelector("#show-user-div")
const container = document.querySelector("#user-div")

btn.addEventListener("click", function(){
    if(container.style.display === "block"){
        container.style.display = "none";
    } else{
        container.style.display = "block";
    }
});

const btn2 = document.querySelector("#show-task-div")
const container2 = document.querySelector("#task-div")

btn2.addEventListener("click", function(){
    if(container2.style.display === "block"){
        container2.style.display = "none";
    } else{
        container2.style.display = "block";
    }
});

const btn3 = document.querySelector("#show-robot-div")
const container3 = document.querySelector("#robot-div")

btn3.addEventListener("click", function(){
    if(container3.style.display === "block"){
        container3.style.display = "none";
    } else{
        container3.style.display = "block";
    }
});
