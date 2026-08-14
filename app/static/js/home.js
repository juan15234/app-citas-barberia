const botones_reserva = document.querySelectorAll(".card .card_info button")

botones_reserva.forEach((boton) => {
    boton.addEventListener("click", () => { 
        window.location.href = "../reservas/" +  boton.id
    })
})