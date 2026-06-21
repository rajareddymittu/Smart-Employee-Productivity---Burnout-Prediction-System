#!/usr/bin/env python
import random
import math
import statistics
from pprint import pprint

print('Starting diagnostics script')

try:
    from app.ml.predict import load_burnout_model, preprocess_features, predict_burnout
except Exception as e:
    print('Import error:', e)
    raise

print('Imports OK')

try:
    model = load_burnout_model()
    print('Model loaded:', type(model))
except Exception as e:
    model = None
    print('Model load failed (will still call predict_burnout):', e)


def gen_sample(seed=None, bias='random'):
    r = random.Random(seed)
    sample = {
        'working_hours_per_day': round(r.uniform(6,10),2),
        'overtime_hours': round(r.uniform(0,6),2),
        'meeting_hours': round(r.uniform(0,6),2),
        'leave_count': r.randint(0,10),
        'late_arrivals': r.randint(0,15),
        'task_count': r.randint(1,20),
        'task_completion_percent': round(r.uniform(30,100),2),
        'performance_rating': round(r.uniform(1.0,5.0),2),
        'experience_years': round(r.uniform(0.0,20.0),2),
        'project_count': r.randint(0,10)
    }
    if bias == 'high_risk':
        sample.update({'overtime_hours': r.uniform(6,12), 'task_completion_percent': r.uniform(10,50), 'performance_rating': r.uniform(1.0,2.5), 'late_arrivals': r.randint(10,30)})
    if bias == 'low_risk':
        sample.update({'overtime_hours': r.uniform(0,1), 'task_completion_percent': r.uniform(85,100), 'performance_rating': r.uniform(4.0,5.0), 'late_arrivals': r.randint(0,2)})
    return sample


def run_batch(n=120):
    samples = []
    for i in range(n):
        if i < 10:
            samples.append(gen_sample(seed=i, bias='low_risk'))
        elif i < 20:
            samples.append(gen_sample(seed=i, bias='high_risk'))
        else:
            samples.append(gen_sample(seed=i))

    results = []
    for s in samples:
        try:
            out = predict_burnout(s)
        except Exception as e:
            out = {'error': str(e)}
        label = None
        score = None
        extra = {}
        if isinstance(out, dict):
            label = out.get('burnout_risk') or out.get('label') or out.get('risk')
            score = out.get('burnout_score') or out.get('score') or out.get('probability') or out.get('prob')
            extra = {k:v for k,v in out.items() if k not in ('burnout_risk','label','risk','burnout_score','score','probability','prob')}
        elif isinstance(out, (list,tuple)) and len(out) >= 1:
            if len(out) >= 2:
                label, score = out[0], out[1]
            else:
                label = out[0]
        else:
            label = str(out)
        raw_prob = None
        try:
            vec = preprocess_features(s)
            if model is not None and hasattr(model, 'predict_proba'):
                probs = model.predict_proba([vec])[0]
                classes = list(model.classes_)
                raw_prob = dict(zip(classes, [float(x) for x in probs]))
        except Exception:
            raw_prob = None
        results.append({'sample': s, 'label': label, 'score': float(score) if (score is not None and isinstance(score,(int,float))) else None, 'raw_prob': raw_prob, 'extra': extra})

    return results


def summarize(results):
    labels = [r['label'] for r in results]
    label_counts = {}
    for L in labels:
        label_counts[L] = label_counts.get(L,0) + 1

    scores = [r['score'] for r in results if r['score'] is not None]

    print('\n=== Label distribution ===')
    pprint(label_counts)

    if scores:
        print('\n=== Score stats (where numeric) ===')
        print('count:', len(scores))
        print('min:', min(scores))
        print('max:', max(scores))
        print('mean:', statistics.mean(scores))
        print('median:', statistics.median(scores))
        print('stdev:', statistics.pstdev(scores))

        numeric_features = ['overtime_hours','task_completion_percent','performance_rating','late_arrivals','working_hours_per_day']
        correlations = {}
        def pearson(xs, ys):
            n = len(xs)
            mx = sum(xs)/n
            my = sum(ys)/n
            num = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
            denx = math.sqrt(sum((x-mx)**2 for x in xs))
            deny = math.sqrt(sum((y-my)**2 for y in ys))
            if denx*deny == 0:
                return None
            return num/(denx*deny)

        for f in numeric_features:
            xs = [r['sample'][f] for r in results if r['score'] is not None]
            ys = [r['score'] for r in results if r['score'] is not None]
            correlations[f] = pearson(xs, ys)

        print('\n=== Pearson correlations (feature vs score) ===')
        pprint(correlations)

    # Sensitivity for overtime
    baseline = gen_sample(seed=999, bias='random')
    ov_vals = [0,1,2,4,6,8,10]
    sens = []
    for v in ov_vals:
        s = baseline.copy()
        s['overtime_hours'] = v
        try:
            out = predict_burnout(s)
        except Exception as e:
            out = {'error': str(e)}
        score = None
        if isinstance(out, dict):
            score = out.get('burnout_score') or out.get('score')
        elif isinstance(out, (list,tuple)) and len(out) >= 2:
            score = out[1]
        sens.append((v, float(score) if score is not None else None))

    print('\n=== Overtime sensitivity (overtime_hours -> score) ===')
    for v,sc in sens:
        print(v, '->', sc)

    print('\n=== Example results (first 6) ===')
    for r in results[:6]:
        pprint({'sample': r['sample'], 'label': r['label'], 'score': r['score'], 'raw_prob': r['raw_prob']})


if __name__ == '__main__':
    res = run_batch(120)
    summarize(res)
    print('\nDiagnostics script finished')
