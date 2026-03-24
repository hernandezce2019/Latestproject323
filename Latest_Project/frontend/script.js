
import user from "./users.js";

const newuser = new user (
    "Cesar",
    "Hernandez",
    113330726,
    "hernandez@gmail.com",
    "Alajuela",
    "May 10, 2025"

 );
const content = `
  <h1>Información de la persona</h1>
  
  <form id="personaForm">
    <label>
      Nombre:
      <input type="text" name="nombre" required />
    </label><br />

    <label>
      Apellido:
      <input type="text" name="apellido" required />
    </label><br />

    

    <label>
      Correo:
      <input type="email" name="correo" required />
    </label><br />

    <label>
      Dirección:
      <input type="text" name="direccion" required />
    </label><br />

    <label>
      Fecha:
      <input type="date" name="fecha" required />
    </label><br /><br />

    <label>
      Contrasena:
      <input type="password" name="contrasena" required />
    </label><br /><br />

    <button type="submit">Guardar Información</button>
  </form>
`;

const main = document.querySelector(".maincontent");
const newArticle = document.createElement("article");
newArticle.setAttribute("id", "newuser");
newArticle.innerHTML = content;
main.appendChild(newArticle);

// Handle form submission
const form = document.getElementById("personaForm");
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  
  const formData = new FormData(form);
  
  const userData = {
    name: formData.get("nombre"),
    surname: formData.get("apellido"),
    email: formData.get("correo"),
    address: formData.get("direccion"),
    date: formData.get("fecha"),
    password: formData.get("contrasena")
  };
  
  try {
    const response = await fetch("http://localhost:8000/users/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(userData)
    });
    
    if (response.ok) {
      const result = await response.json();
      alert("Usuario guardado exitosamente!");
      form.reset();
      console.log("User saved:", result);
    } else {
      const error = await response.json();
      alert("Error: " + (error.detail || "No se pudo guardar el usuario"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("Error en la conexión con el servidor");
  }
});