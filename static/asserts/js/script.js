


    /* =========================
       ОТКРЫТИЕ КОРЗИНЫ
    ========================= */
    document.querySelector(".cart-btn").onclick = () => {
        document.getElementById("cartPanel").classList.toggle("open");
    };


    document.getElementById("close_trash").onclick = () => {
        document.getElementById("cartPanel").classList.toggle("open");
    };

    function close_trash() {
        document.getElementById("cartPanel").classList.toggle("open");
    }

    async function get_categories() {
        let response = await fetch("http://localhost:8000/api/v1/categories");
        return response;
    }

    get_categories().then(async response => {
        let categories = document.getElementById("categories");
        let txt = "";

        if (response.ok) {
            let data = await response.json();   // дождаться JSON
            console.log(data);

            let count = data.length;
            for (let i = 0; i < count; i++) {
                txt += `<a href="http://localhost:8000/api/v1/categories/${data[i].id}">${data[i].name}</a>`;
            }
        } else {
            console.error("Ошибка HTTP: " + response.status);
        }

        categories.innerHTML = txt;
    });

    const slides = document.querySelector('.slides');
    const slideCount = document.querySelectorAll('.slide').length;
    let index = 0;

    function showSlide(i) {
        index = (i + slideCount) % slideCount;
        slides.style.transform = `translateX(-${index * 100}%)`;
    }

    document.getElementById('next').addEventListener('click', () => {
        showSlide(index + 1);
    });

    document.getElementById('prev').addEventListener('click', () => {
        showSlide(index - 1);
    });

    // Автоматическая прокрутка каждые 3 секунды
    setInterval(() => {
        showSlide(index + 1);
    }, 3000);

