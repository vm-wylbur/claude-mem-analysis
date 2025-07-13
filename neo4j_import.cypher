// Clear any existing data
MATCH (n) DETACH DELETE n;

// Load memories with real data structure  
LOAD CSV WITH HEADERS FROM 'file:///memories.csv' AS row
CREATE (m:Memory {
    id: row.memory_id,
    content: row.content_clean,
    type: row.content_type,
    created_at_raw: row.created_at,
    created_date: split(row.created_at, ' ')[0],
    tags: row.tags,
    sentiment: row.sentiment,
    complexity: row.complexity,
    content_preview: left(row.content_clean, 100) + '...',
    length: size(row.content_clean)
});

// Create index for better performance
CREATE INDEX memory_id_index IF NOT EXISTS FOR (m:Memory) ON (m.id);
CREATE INDEX memory_created_index IF NOT EXISTS FOR (m:Memory) ON (m.created_at_raw);

// Create temporal relationships between consecutive memories
MATCH (m:Memory)
WITH m ORDER BY m.created_at_raw
WITH collect(m) as memories
FOREACH(i in range(0, size(memories)-2) | 
    FOREACH(m1 in [memories[i]] | 
        FOREACH(m2 in [memories[i+1]] |
            CREATE (m1)-[:FOLLOWS]->(m2)
        )
    )
);

// Extract tags and create tag nodes
MATCH (m:Memory)
WHERE m.tags <> '[]' AND m.tags IS NOT NULL
WITH m, split(replace(replace(m.tags, '[', ''), ']', ''), ',') as tag_list
UNWIND tag_list as tag_raw
WITH m, trim(replace(tag_raw, '"', '')) as clean_tag
WHERE clean_tag <> ''
MERGE (t:Tag {name: clean_tag})
CREATE (m)-[:HAS_TAG]->(t);

// Create problem cascade relationships
MATCH (m1:Memory)-[:FOLLOWS]->(m2:Memory)
WHERE m1.sentiment = 'positive' AND m2.sentiment = 'negative'
CREATE (m1)-[:POTENTIAL_CAUSE]->(m2);

// Return count to verify
MATCH (n) RETURN count(n) as totalNodes;