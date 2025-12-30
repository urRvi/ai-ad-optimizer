import { useState } from "react";
import { generate } from "./lib/api";

export default function App(){
  const [form, setForm] = useState({product:"", audience:"", tone:"Professional", keywords:"", variants:5, include_lp:true});
  const [data, setData] = useState(null);
  const [loading,setLoading]=useState(false);

  const onChange = e => setForm({...form, [e.target.name]: e.target.type === "number" ? Number(e.target.value) : e.target.value});
  const submit = async () => {
    setLoading(true);
    try{ setData(await generate(form)); } finally{ setLoading(false); }
  };

  return (
    <div style={{maxWidth:900, margin:"40px auto", fontFamily:"Inter, system-ui"}}>
      <h1>AI Ad & LP Optimizer</h1>
      <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:12}}>
        <input name="product" placeholder="Product" onChange={onChange}/>
        <input name="audience" placeholder="Audience" onChange={onChange}/>
        <input name="tone" placeholder="Tone" onChange={onChange} defaultValue={form.tone}/>
        <input name="keywords" placeholder="Keywords" onChange={onChange}/>
        <input name="variants" type="number" min="1" max="7" onChange={onChange} defaultValue={5}/>
      </div>
      <button onClick={submit} disabled={loading} style={{marginTop:16}}>{loading?"Generating...":"Generate"}</button>

      {data && (
        <div style={{marginTop:24}}>
          <h2>Ad Variants</h2>
          <ul>
            {data.variants.map((v,i)=> (
              <li key={i} style={{marginBottom:12}}>
                <strong>{v.headline}</strong><br/>
                <span>{v.description}</span><br/>
                <em>CTA: {v.cta}</em>
              </li>
            ))}
          </ul>
          {data.landing && (
            <div>
              <h2>Landing Page Sections</h2>
              <pre>{JSON.stringify(data.landing,null,2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
