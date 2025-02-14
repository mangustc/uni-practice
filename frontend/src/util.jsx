export const DeepClone = function (obj) {
  return structuredClone(obj);
};

export const GetSetObjectAttrtibuteFunc = function (setObj) {
  return function (key, value) {
    setObj((obj) => {
      const newObj = { ...obj };
      newObj[key] = value;
      return newObj;
    });
  };
};
