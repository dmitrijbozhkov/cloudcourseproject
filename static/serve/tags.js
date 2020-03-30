let st = [{label: 'Alabama', value: 'AL'}, {label: 'Wyoming', value: 'WY'}];
bulmahead('input-id', 'menu-id', v => new Promise((rs,rj) => rs(st.filter(s=>s.startsWith(v))), 200, 2));