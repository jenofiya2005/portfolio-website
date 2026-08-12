$(document).ready(function () {
  $.get("/api/projects", function (projects) {
    const container = $("#project-list");
    container.empty();

    if (!projects || projects.length === 0) {
      container.html("<p class='loading-text'>No projects yet.</p>");
      return;
    }

    projects.forEach(function (p) {
      const techTags = (p.tech || "")
        .split(",")
        .map((t) => `<span class="tag">${t.trim()}</span>`)
        .join("");

      const card = `
        <div class="col-md-6 col-lg-4">
          <div class="project-card">
            <div class="project-card-body">
              <h3>${p.title}</h3>
              <p class="project-desc">${p.description}</p>
              <div class="tag-row">${techTags}</div>
              <div class="project-links">
                ${p.github ? `<a href="${p.github}" target="_blank" rel="noopener">GitHub &rarr;</a>` : ""}
                ${p.live ? `<a href="${p.live}" target="_blank" rel="noopener">Live &rarr;</a>` : ""}
              </div>
            </div>
          </div>
        </div>`;
      container.append(card);
    });
  }).fail(function () {
    $("#project-list").html("<p class='loading-text'>Couldn't load projects right now.</p>");
  });
});
