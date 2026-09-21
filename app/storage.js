/* Hosted state stays on this browser; local Python mode retains disk storage. */
window.atlasStorage = {
  key: 'aiml-atlas-progress-v1',
  read() {
    try {
      const value = JSON.parse(localStorage.getItem(this.key) || '{}');
      return value && typeof value === 'object' ? value : {};
    } catch { return {}; }
  },
  restore(library) {
    const saved = this.read();
    const validTasks = new Set(library.stages.flatMap((s,i)=>s.tasks.map((_,j)=>`${i}-${j}`)));
    library.completedTasks = Array.isArray(saved.completedTasks) ? saved.completedTasks.filter(id=>validTasks.has(id)) : [];
    for (const resource of library.resources) {
      const prior = saved.resources?.[resource.id];
      if (prior && ['saved','reading','complete'].includes(prior.status) && typeof prior.notes === 'string') {
        resource.status=prior.status; resource.notes=prior.notes.slice(0,20000);
      }
    }
    return library;
  },
  save(library, payload) {
    const snapshot = { completedTasks:[...library.completedTasks], resources:Object.fromEntries(library.resources.map(r=>[r.id,{status:r.status,notes:r.notes}])) };
    if (payload.type==='task') {
      snapshot.completedTasks=snapshot.completedTasks.filter(id=>id!==payload.id);
      if(payload.done) snapshot.completedTasks.push(payload.id);
    } else if(payload.type==='resource') snapshot.resources[payload.id]={status:payload.status,notes:payload.notes};
    try { localStorage.setItem(this.key,JSON.stringify(snapshot)); }
    catch { throw Error('Your browser could not save this change. Enable site storage or export your library as a backup.'); }
  }
};
