// Course card animation
const courseCards = document.querySelectorAll('.course-card');
let courseSectionAnimated = false;

function showCourseCards() {
  courseCards.forEach((card, index) => {
    setTimeout(() => {
      card.classList.add('show');
    }, index * 200);
  });
}

window.addEventListener('scroll', () => {
  const courseSection = document.querySelector('.course-section');
  const courseSectionTop = courseSection.offsetTop;
  const courseSectionHeight = courseSection.offsetHeight;
  const windowHeight = window.innerHeight;

  if (!courseSectionAnimated && window.scrollY >= courseSectionTop - windowHeight + courseSectionHeight / 2) {
    showCourseCards();
    courseSectionAnimated = true;
  }
});


window.addEventListener('load', animateElements);
