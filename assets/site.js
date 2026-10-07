function syncTopicParents() {
  document.querySelectorAll('[data-family-toggle]').forEach((parent) => {
    const children = [...document.querySelectorAll(`[data-topic-family="${parent.dataset.familyToggle}"]`)];
    const selected = children.filter((child) => child.checked).length;
    parent.checked = selected === children.length;
    parent.indeterminate = selected > 0 && selected < children.length;
  });
}

function venueTopicMatch(row) {
  const selected = [...document.querySelectorAll('[data-topic-family]:checked')];
  const families = new Map();
  selected.forEach((input) => {
    const group = families.get(input.dataset.topicFamily) || [];
    group.push(input.value);
    families.set(input.dataset.topicFamily, group);
  });
  const topics = row.dataset.topics.split(' ');
  const centralFamilies = (row.dataset.families || '').split(' ');
  const matches = [...families.entries()].map(([family, group]) => {
    const parent = document.querySelector(`[data-family-toggle="${family}"]`);
    return parent.checked ? centralFamilies.includes(family)
      : group.some((topic) => topics.includes(topic));
  });
  if (document.querySelector('#time-series-shortcut').checked) {
    matches.push(topics.includes('time-series-sequential-data'));
  }
  if (!matches.length) return true;
  return document.querySelector('#topic-match').value === 'all'
    ? matches.every(Boolean) : matches.some(Boolean);
}

let conferenceMap;
let cityMarkers;
let lastMapSignature;
const worldMapBounds = [[-60, -180], [80, 180]];

function resetConferenceMap() {
  conferenceMap.closePopup();
  conferenceMap.fitBounds(worldMapBounds, {padding: [12, 12], animate: false});
}

function updateConferenceMap() {
  if (document.querySelector('#panel-conferences').hidden) return;
  if (!conferenceMap) {
    conferenceMap = L.map('conference-map', {
      crs: L.CRS.EPSG4326, minZoom: -1, maxZoom: 7, zoomSnap: .25,
      scrollWheelZoom: false, worldCopyJump: false,
      // Leave enough room for popup auto-pan at the full-world zoom.
      maxBounds: [[-180, -360], [180, 360]], maxBoundsViscosity: .8,
    }).fitBounds(worldMapBounds, {padding: [12, 12]});
    L.geoJSON(venueMapData.land, {interactive: false, style: {
      color: '#bdccce', weight: .7, fillColor: '#e3ebeb', fillOpacity: 1,
    }}).addTo(conferenceMap);
    conferenceMap.attributionControl.addAttribution('Land: <a href="https://www.naturalearthdata.com/">Natural Earth</a>');
    cityMarkers = L.layerGroup().addTo(conferenceMap);
    conferenceMap.on('resize', resetConferenceMap);
    const reset = L.control({position: 'topleft'});
    reset.onAdd = () => {
      const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control-reset');
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'leaflet-reset-world';
      button.title = 'Reset world view';
      button.setAttribute('aria-label', 'Reset world view');
      button.innerHTML = venueMapData.resetIcon;
      button.addEventListener('click', resetConferenceMap);
      container.append(button);
      L.DomEvent.disableClickPropagation(container);
      return container;
    };
    reset.addTo(conferenceMap);
  }
  conferenceMap.invalidateSize();
  const now = Date.now();
  const visibleIds = new Set([...document.querySelectorAll('[data-conference-row]')]
    .filter((row) => !row.hidden).map((row) => row.dataset.edition));
  const events = venueMapData.events.filter((event) =>
    Date.parse(`${event.start}T00:00:00Z`) > now && visibleIds.has(event.id));
  const signature = events.map((event) => event.id).join('|');
  if (signature === lastMapSignature) return;
  lastMapSignature = signature;
  cityMarkers.clearLayers();
  const byCity = new Map();
  events.forEach((event) => {
    const group = byCity.get(event.city) || [];
    group.push(event);
    byCity.set(event.city, group);
  });
  const list = document.querySelector('#map-cities');
  list.replaceChildren();
  byCity.forEach((group) => {
    const city = group[0];
    const popup = document.createElement('div');
    popup.className = 'city-popup';
    const heading = document.createElement('strong');
    heading.textContent = city.label;
    popup.append(heading);
    const entries = document.createElement('ul');
    group.forEach((event) => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = event.url;
      link.textContent = event.title;
      const dates = document.createElement('time');
      dates.dateTime = event.start;
      const formatter = new Intl.DateTimeFormat('en', {month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC'});
      dates.textContent = `${formatter.format(new Date(event.start))} - ${formatter.format(new Date(event.end))}`;
      item.append(link, dates);
      entries.append(item);
    });
    popup.append(entries);
    const marker = L.marker([city.lat, city.lon], {keyboard: true,
      title: `${city.label}: ${group.map((event) => event.title).join(', ')}`,
      alt: `${city.label}, ${group.length} upcoming conference${group.length === 1 ? '' : 's'}`,
      icon: L.divIcon({className: 'city-marker', iconSize: [12, 12], iconAnchor: [6, 6]}),
    }).bindPopup(popup, {maxWidth: 290, maxHeight: 180, autoPanPadding: [12, 12]}).addTo(cityMarkers);
    marker.on('mouseover', () => marker.openPopup());
    marker.on('add', () => {
      marker.getElement().setAttribute('aria-label', marker.options.alt);
    });
    marker.getElement()?.setAttribute('aria-label', marker.options.alt);
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'map-city-link';
    button.textContent = `${city.label} (${group.length})`;
    button.addEventListener('click', () => {
      conferenceMap.setView(marker.getLatLng(), Math.max(3, conferenceMap.getZoom()), {animate: false});
      marker.openPopup();
    });
    list.append(button);
  });
  document.querySelector('#map-count').textContent = `${events.length} confirmed editions in ${byCity.size} cities`;
  document.querySelector('#map-empty').hidden = events.length > 0;
}

function loadCommunityComments() {
  if (document.querySelector('.giscus script')) return;
  const script = document.createElement('script');
  script.src = 'https://giscus.app/client.js';
  const settings = {
    repo: 'gon-uri/venue-radar', 'repo-id': 'R_kgDOTQKmZg',
    category: 'Announcements', 'category-id': 'DIC_kwDOTQKmZs4DHLTi',
    mapping: 'specific', term: 'Venue Radar community', strict: '1',
    'reactions-enabled': '1', 'emit-metadata': '0', 'input-position': 'top',
    theme: 'light', lang: 'en', loading: 'lazy',
  };
  Object.entries(settings).forEach(([key, value]) => script.setAttribute(`data-${key}`, value));
  script.crossOrigin = 'anonymous';
  script.async = true;
  document.querySelector('.giscus').append(script);
}
