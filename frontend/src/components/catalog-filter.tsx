import * as util from "../util.tsx";
import * as objects from "../objects.tsx";

function CatalogFilter({
  filters,
  setFilters,
  updateFilters: updateFilters,
  properties,
  colors,
  priceMax,
  priceMin,
}: {
  filters: objects.CatalogFilters;
  setFilters: React.Dispatch<any>;
  updateFilters: (newFilters: objects.CatalogFilters) => void;
  properties: objects.Property[];
  colors: objects.Color[];
  priceMax: number;
  priceMin: number;
}) {
  return (
    <div className="catalog-filter-container">
      <div className="catalog-filter-block">
        <h6>Наличие товара</h6>
        <div className="catalog-radio-line" style={{gap: "12px", cursor: "pointer"}}
            onClick={() =>
              setFilters({
                ...filters,
                productOnlyInStock: false,
              })
            }
        >
          <input type="radio" checked={!filters.productOnlyInStock} />
          <label id="radio-label" style={{cursor: "pointer"}}>Все товары</label>
        </div>
 
        <div className="catalog-radio-line" style={{gap: "12px", cursor: "pointer"}}
          onClick={() =>
            setFilters({
              ...filters,
              productOnlyInStock: true,
            })
          }
        >
          <input type="radio" checked={filters.productOnlyInStock} />
          <label id="radio-label" style={{cursor: "pointer"}}>В наличии</label>
        </div>
      </div>
      <div className="catalog-filter-block">
        <h6>Цена, руб</h6>
        <div className="catalog-filter-line" style={{gap: "12px"}}>
        <input
          type="number"
          className="price-input"
          placeholder={String(priceMin)}
          value={
            filters.productPriceStart === 0 ? "" : filters.productPriceStart
          }
          onChange={(e) =>
            setFilters({
              ...filters,
              productPriceStart: util.Num(e.target.value),
            })
          }
        />
        <input
          type="number"
          className="price-input"
          placeholder={String(priceMax)}
          value={filters.productPriceEnd === 0 ? "" : filters.productPriceEnd}
          onChange={(e) =>
            setFilters({
              ...filters,
              productPriceEnd: util.Num(e.target.value),
            })
          }
        />
        </div>
      </div>
      <div className="catalog-filter-block">
        <h6>Цвет</h6>
        {colors.map((color) => (
          <div
            key={color.colorID}
            className="catalog-filter-line" style={{gap:"12px"}}
          >
            <input
              type="checkbox"
              checked={filters.colors.includes(color.colorID)}
              onChange={(e) => {
                const newColors = structuredClone(filters.colors);
                e.target.checked
                  ? newColors.push(color.colorID)
                  : newColors.splice(newColors.indexOf(color.colorID), 1);

                setFilters({ ...filters, colors: newColors });
              }}
            />
            <label>{color.colorName}</label>
            
          </div>
        ))}
      </div>
      {properties.map((property) => {
        let filterPropertyIndex = -1;
        for (let i = 0; i < filters.properties.length; i++) {
          if (filters.properties[i].propertyID == property.propertyID) {
            filterPropertyIndex = i;
            break;
          }
        }
        if (filterPropertyIndex == -1) {
          filterPropertyIndex = filters.properties.length;
          filters.properties.push({
            propertyID: property.propertyID,
            propertyValues: [],
          });
        }
        return (
          <div className="catalog-filter-block"
            key={property.propertyID}
            style={{ display: "flex", flexDirection: "column" }}
          >
            <h6>{property.propertyName}</h6>
            {property.propertyValues.map((value) => (
              <div
                key={
                  String(filters.properties[filterPropertyIndex].propertyID) +
                  value
                }
                className="catalog-filter-line" style={{gap:"12px"}}
              >
                
                <input
                  type="checkbox"
                  checked={filters.properties[
                    filterPropertyIndex
                  ].propertyValues.includes(value)}
                  onChange={(e) => {
                    const newProperties = structuredClone(filters.properties);
                    e.target.checked
                      ? newProperties[filterPropertyIndex].propertyValues.push(
                          value,
                        )
                      : newProperties[
                          filterPropertyIndex
                        ].propertyValues.splice(
                          newProperties[
                            filterPropertyIndex
                          ].propertyValues.indexOf(value),
                          1,
                        );

                    setFilters({ ...filters, properties: newProperties });
                  }}
                />
                <label>{value}</label>
              </div>
            ))}
          </div>
        );
      })}
      <button onClick={() => updateFilters(structuredClone(filters))} className="catalog-filter-btn-done">
        Применить
      </button>
      <button className="catalog-filter-btn-reset">Сбросить</button>
    </div>
  );
}

export default CatalogFilter;
